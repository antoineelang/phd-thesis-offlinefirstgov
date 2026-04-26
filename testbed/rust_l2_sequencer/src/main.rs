use sha2::{Sha256, Digest};
use std::collections::VecDeque;
use std::time::Duration;
use tokio::time::sleep;

/// Represents a digitized civic transaction (e.g., BUNEC birth registration)
#[derive(Clone, Debug)]
struct Transaction {
    id: String,
    payload: String,
}

/// 1. The Mempool: Ingests and orders civic transactions offline
struct Mempool {
    queue: VecDeque<Transaction>,
}

impl Mempool {
    fn new() -> Self {
        Mempool { queue: VecDeque::new() }
    }
    fn add_tx(&mut self, tx: Transaction) {
        self.queue.push_back(tx);
    }
}

/// 2. & 3. The Sequencer: Handles Batching and the State Transition Function (STF)
struct L2Sequencer {
    mempool: Mempool,
    current_state: String,
}

impl L2Sequencer {
    fn new() -> Self {
        L2Sequencer {
            mempool: Mempool::new(),
            current_state: "GENESIS_STATE_000000000000".to_string(),
        }
    }

    /// ACTION a1 (COMPUTE): Generates the Merkle Root for pending transactions
    async fn compute_merkle_stf(&mut self) {
        println!("[RUST] Executing Action a1: COMPUTE");
        if self.mempool.queue.is_empty() {
            println!("       -> Mempool empty, nothing to compute.");
            return;
        }

        println!("       -> Batching {} transactions...", self.mempool.queue.len());
        let mut hasher = Sha256::new();
        
        // Simulated Merkle Tree Construction O(N log N)
        for tx in &self.mempool.queue {
            hasher.update(tx.id.as_bytes());
        }
        let result = hasher.finalize();
        let merkle_root = format!("{:x}", result);
        
        // Update State
        self.current_state = merkle_root.clone();
        println!("       -> STF Complete. New Merkle Root: {}", merkle_root);
        
        // Clear mempool after batching
        self.mempool.queue.clear();
    }

    /// ACTION a2 (SYNCHRONIZE): Transmits the ~52KB payload to L1 and triggers DAG-DSR
    async fn synchronize_to_l1(&self) {
        println!("[RUST] Executing Action a2: SYNCHRONIZE");
        println!("       -> Waking 4G Modem (SIM7600E)...");
        println!("       -> Constructing ~52 KB payload (Merkle Root + VDF Proof + Metadata)");
        
        // Simulate network delay and timeout bounds (T_sync = 30s)
        sleep(Duration::from_millis(500)).await;
        
        println!("       -> Payload broadcasted to Layer 1 Smart Contract.");
        println!("       -> ACK received! Triggering DAG-DSR Reconciliation (Article 2 logic).");
    }

    /// ACTION a0 (SLEEP): Halts heavy cryptography
    async fn sleep_mode(&self) {
        println!("[RUST] Executing Action a0: SLEEP");
        println!("       -> Hardware halted. Queuing incoming Tx to low-power RAM only.");
    }
}

/// Simulated RPC Server listening for the Python DRL Orchestrator
#[tokio::main]
async fn main() {
    println!("=======================================================");
    println!(" L2 Edge Sequencer (Rust) - Offline-First Gov Project");
    println!("=======================================================\n");

    let mut sequencer = L2Sequencer::new();

    // Simulate some offline civic registrations arriving from the village
    sequencer.mempool.add_tx(Transaction { id: "TX_BIRTH_991".to_string(), payload: "Data".to_string() });
    sequencer.mempool.add_tx(Transaction { id: "TX_MARRIAGE_992".to_string(), payload: "Data".to_string() });

    println!("[RPC] Listening for Python DRL Agent Commands on port 50051...");
    
    // Simulating incoming RPC commands from the Python DRL Orchestrator
    // In reality, this would be a gRPC or TCP listener loop.
    let incoming_actions = vec![1, 0, 2]; // Compute, Sleep, Sync
    
    for action in incoming_actions {
        sleep(Duration::from_secs(1)).await;
        println!("\n[RPC] Received command from Python Orchestrator: {}", action);
        match action {
            1 => sequencer.compute_merkle_stf().await,
            2 => sequencer.synchronize_to_l1().await,
            0 => sequencer.sleep_mode().await,
            _ => println!("Unknown command."),
        }
    }
}
