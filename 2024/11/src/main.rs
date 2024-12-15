use std::str::FromStr;
use std::io::BufRead;
use std::collections::HashMap;

fn process_stones(iteration: i32, stone: i64, cache: &mut HashMap<(i32, i64), i64>) -> i64 {
    if iteration == 0 {
        return 1;
    }

    if let Some(count) = cache.get(&(iteration, stone)) {
        return *count;
    }

    let mut result = 0;
    if stone == 0 {
        result = process_stones(iteration - 1, 1, cache);
    } else {
        let size = stone.ilog10() + 1;
        if size % 2 == 0 {
            let divider = 10_i64.pow(size / 2);
            result += process_stones(iteration - 1, stone % divider, cache);
            result += process_stones(iteration - 1, stone / divider, cache);
        } else {
            result = process_stones(iteration - 1, stone * 2024, cache);
        }
    }

    cache.insert((iteration, stone), result);
    return result
}

fn main() {
    let stdin = std::io::stdin().lock();
    let line = stdin.lines().next().unwrap().unwrap();
    let mut cache: HashMap<(i32, i64), i64> = HashMap::new();

    let count: i64 = line.split(" ")
        .map(|stone| (25, i64::from_str(stone).unwrap()))
        .map(|(iteration, stone)| process_stones(iteration, stone, &mut cache))
        .sum();
    println!("[Part one] {} stones", count);

    let count: i64 = line.split(" ")
        .map(|stone| (75, i64::from_str(stone).unwrap()))
        .map(|(iteration, stone)| process_stones(iteration, stone, &mut cache))
        .sum();
    println!("[Part two] {} stones", count);
}
