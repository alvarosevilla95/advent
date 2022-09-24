// https://adventofcode.com/2021/day/16

use crate::utils::*;
use macroquad::prelude::*;

// The transmission was sent using the Buoyancy Interchange Transmission System (BITS),
// a method of packing numeric expressions into a binary sequence. Your submarine's
// computer has saved the transmission in hexadecimal (your puzzle input).
pub async fn run() {
    let input = get_input(16).await.strip_suffix("\n").unwrap().to_owned();
    let _input = "9C0141080250320F1802104A08";
    let bytes = hex::decode(input).unwrap();
    let packet = Packet::from_bytes(&mut BitReader::new(bytes));
    // Part 1
    // Decode the structure of your hexadecimal-encoded BITS transmission;
    // what do you get if you add up the version numbers in all packets?
    info!("{:?}", packet.version_sum());
    // Part 2
    // What do you get if you evaluate the expression represented by your
    // hexadecimal-encoded BITS transmission?
    info!("{}", packet.eval());
}

#[derive(Debug)]
struct Packet {
    ptype: i64,
    version: i64,
    value: i64,
    subpackets: Vec<Packet>,
}

impl Packet {
    fn from_bytes(bits: &mut BitReader) -> Packet {
        let version = bits.read(3);
        let ptype = bits.read(3);
        if ptype == 4 {
            Packet {
                version,
                ptype,
                value: Packet::literal(bits),
                subpackets: vec![],
            }
        } else {
            Packet {
                version,
                ptype,
                value: 0,
                subpackets: if bits.read(1) == 0 {
                    Packet::length_operator(bits)
                } else {
                    Packet::counter_operator(bits)
                },
            }
        }
    }

    fn literal(bits: &mut BitReader) -> i64 {
        let mut n = 0 as i64;
        loop {
            let flag = bits.read(1);
            let next_bits = bits.read(4);
            n = (n << 4) + next_bits as i64;
            if flag == 0 {
                break;
            }
        }
        n
    }

    fn length_operator(bits: &mut BitReader) -> Vec<Packet> {
        let length = bits.read(15) as usize;
        let mut packets = vec![];
        let offset = bits.counter() + length;
        while bits.counter() < offset {
            packets.push(Packet::from_bytes(bits));
        }
        packets
    }

    fn counter_operator(bits: &mut BitReader) -> Vec<Packet> {
        let count = bits.read(11) as usize;
        let mut packets = Vec::with_capacity(count);
        for _ in 0..count {
            packets.push(Packet::from_bytes(bits));
        }
        packets
    }
    fn version_sum(&self) -> i64 {
        self.version + self.subpackets.iter().map(|p| p.version_sum()).sum::<i64>()
    }

    fn eval(&self) -> i64 {
        let mut subs = self.subpackets.iter().map(|p| p.eval());
        let v = match self.ptype {
            0 => subs.sum::<i64>(),
            1 => subs.product::<i64>(),
            2 => subs.min().unwrap(),
            3 => subs.max().unwrap(),
            4 => self.value,
            5 => (subs.next().unwrap() > subs.next().unwrap()) as i64,
            6 => (subs.next().unwrap() < subs.next().unwrap()) as i64,
            7 => (subs.next().unwrap() == subs.next().unwrap()) as i64,
            _ => panic!("couldn't parse packet"),
        };
        v
    }
}
