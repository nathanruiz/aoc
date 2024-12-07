use std::collections::HashSet;
use std::collections::HashMap;
use std::collections::hash_map::Entry;
use std::io::BufRead;

#[derive(Debug)]
struct LoopError {}

#[derive(Debug, Clone, Copy)]
struct Vector {
    dx: i32,
    dy: i32,
}

impl Vector {
    fn new(dx: i32, dy: i32) -> Self {
        Self { dx, dy }
    }
}

#[derive(Debug, Clone, Copy, Hash, PartialOrd, Ord, PartialEq, Eq)]
struct Position {
    x: i32,
    y: i32,
}

impl Position {
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }

    fn add(&self, vec: Vector) -> Self {
        Self {
            x: self.x + vec.dx,
            y: self.y + vec.dy,
        }
    }
}

#[derive(Debug, Clone, Copy, Hash, PartialOrd, Ord, PartialEq, Eq)]
enum Direction {
    Right,
    Left,
    Up,
    Down,
}

impl From<u8> for Direction {
    fn from(value: u8) -> Direction {
        match value {
            b'>' => Direction::Right,
            b'<' => Direction::Left,
            b'^' => Direction::Up,
            b'v' => Direction::Down,
            _ => panic!("Unexpected direction character '{}'", value),
        }
    }
}

impl Into<u8> for Direction {
    fn into(self) -> u8 {
        match self {
            Direction::Right => b'>',
            Direction::Left => b'<',
            Direction::Up => b'^',
            Direction::Down => b'v',
        }
    }
}

impl From<&Direction> for Vector {
    fn from(value: &Direction) -> Vector {
        match value {
            Direction::Right => Vector::new(1, 0),
            Direction::Left => Vector::new(-1, 0),
            Direction::Up => Vector::new(0, -1),
            Direction::Down => Vector::new(0, 1),
        }
    }
}

impl Direction {
    fn translate(&self, position: Position) -> Position {
        position.add(self.into())
    }

    fn turn_right(&self) -> Self {
        match self {
            Direction::Right => Direction::Down,
            Direction::Left => Direction::Up,
            Direction::Up => Direction::Right,
            Direction::Down => Direction::Left,
        }
    }
}

#[derive(Clone, Copy)]
enum Tile {
    Start(Direction),
    Obstruction,
    Empty,
}

impl From<u8> for Tile {
    fn from(value: u8) -> Tile {
        match value {
            b'>' | b'<' | b'^' | b'v' => Tile::Start(value.into()),
            b'#' => Tile::Obstruction,
            _ => Tile::Empty,
        }
    }
}

struct Map {
    lines: Vec<Vec<Tile>>,
    position: Position,
    direction: Direction,
    visited: HashMap<(Position, Direction), ()>,
}

impl Map {
    fn new(lines: Vec<Vec<Tile>>) -> Self {
        let mut map = Self {
            lines,
            position: Position::new(0, 0),
            direction: Direction::Right,
            visited: HashMap::new(),
        };
        let (position, direction) = map.get_starting_point();
        map.position = position;
        map.direction = direction;
        map
    }

    fn get(&self, position: Position) -> Tile {
        self.lines[position.y as usize][position.x as usize]
    }

    fn set(&mut self, position: Position, tile: Tile) {
        self.lines[position.y as usize][position.x as usize] = tile;
    }

    fn get_bounds(&self) -> (i32, i32) {
        return (self.lines[0].len() as i32, self.lines.len() as i32)
    }

    fn is_in_bounds(&self, position: Position) -> bool {
        let (x, y) = (position.x, position.y);
        let (mx, my) = self.get_bounds();
        return x >= 0 && x < mx && y >= 0 && y < my;
    }

    fn get_starting_point(&self) -> (Position, Direction) {
        let (mx, my) = self.get_bounds();
        for x in 0..mx {
            for y in 0..my {
                let position = Position::new(x, y);
                match self.get(position) {
                    Tile::Start(direction) => return (position, direction),
                    _ => {},
                }
            }
        }
        panic!("Couldn't find guard starting position");
    }

    fn simulate(&mut self) -> Result<(), LoopError> {
        loop {
            match self.visited.entry((self.position, self.direction)) {
                Entry::Occupied(_) => return Err(LoopError {}),
                Entry::Vacant(entry) => entry.insert(()),
            };
            //if self.visited.contains(&(self.position, self.direction)) {
            //    return Err(LoopError {});
            //}

            // self.visited.insert((self.position, self.direction));

            let position = self.direction.translate(self.position);
            if !self.is_in_bounds(position) {
                break;
            }

            match self.get(position) {
                Tile::Obstruction => {
                    self.direction = self.direction.turn_right();
                    continue;
                }
                _ => {},
            }

            self.position = position;
        }
        Ok(())
    }

    /// Count the number of visited positions. This must be done after the
    /// simulation is complete.
    fn count_positions(&self) -> i32 {
        if self.visited.is_empty() {
            panic!("Simulation hasn't been run yet");
        }

        let positions: HashSet<Position> = self.visited
            .iter()
            .map(|((pos, _), _)| *pos)
            .collect();

        positions.len() as i32
    }

    fn count_loopers(&self) -> i32 {
        if self.visited.is_empty() {
            panic!("Simulation hasn't been run yet");
        }

        let mut obstructions: HashSet<Position> = self.visited
            .iter()
            .map(|((position, direction), _)| direction.translate(*position))
            .collect();
        obstructions.remove(&self.get_starting_point().0);

        let mut count = 0;
        for position in obstructions.into_iter() {
            if self.is_in_bounds(position) {
                let mut new_map = self.with_extra_obstruction(position);
                match new_map.simulate() {
                    Ok(_) => {},
                    Err(LoopError {}) => count += 1,
                }
            }
        }

        count
    }

    fn render(&self) {
        let visited: HashSet<Position> = self.visited
            .iter()
            .map(|((pos, _), _)| *pos)
            .collect();

        let (mx, my) = self.get_bounds();
        for y in 0..my {
            for x in 0..mx {
                let position = Position::new(x, y);

                if visited.contains(&position) {
                    print!("@");
                    continue;
                }

                match self.get(position) {
                    Tile::Start(direction) => {
                        let byte: u8 = direction.into();
                        print!("{}", byte as char);
                    },
                    Tile::Empty => print!("."),
                    Tile::Obstruction => print!("#"),
                }
            }
            print!("\n");
        }
        print!("\n");
    }

    fn with_extra_obstruction(&self, position: Position) -> Map {
        let lines = self.lines.clone();
        let mut map = Map::new(lines);
        map.set(position, Tile::Obstruction);
        map
    }
}

fn main() {
    let mut lines : Vec<Vec<u8>> = Vec::new();
    for line in std::io::stdin().lock().lines() {
        let line_bytes: Vec<u8> = line.unwrap().into_bytes();
        lines.push(line_bytes);
    }

    let lines: Vec<Vec<Tile>> = lines
        .into_iter()
        .map(|line| line.into_iter().map(|tile| tile.into()).collect())
        .collect();

    let mut map = Map::new(lines);
    map.simulate().unwrap();
    println!("[Part one] Number of locations: {}", map.count_positions());
    println!("[Part two] Number of loops: {}", map.count_loopers());
}
