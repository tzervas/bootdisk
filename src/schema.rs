use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::Path;

#[derive(Debug, Deserialize, Serialize)]
pub struct Project {
    pub project: String,
    pub version: String,
    pub description: String,
    pub languages: Vec<String>,
    pub frameworks: Vec<String>,
    pub agents: Vec<Agent>,
    pub workflows: Vec<Workflow>,
    pub quality_gates: QualityGates,
    pub hardware_spec: HardwareSpec,
    pub debian_config: DebianConfig,
    pub storage_layout: StorageLayout,
    pub network_config: NetworkConfig,
    pub security_config: SecurityConfig,
    pub development_config: DevelopmentConfig,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Agent {
    pub role: String,
    pub enabled: bool,
    pub capabilities: Vec<String>,
    pub model: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Workflow {
    pub name: String,
    pub description: String,
    pub stages: Vec<String>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct QualityGates {
    pub test_coverage: u32,
    pub linting: bool,
    pub security_scanning: bool,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct HardwareSpec {
    pub motherboard: String,
    pub bios_version: String,
    pub bios_date: String,
    pub cpu: String,
    pub gpu: String,
    pub ram: String,
    pub storage: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct DebianConfig {
    pub version: String,
    pub codename: String,
    pub package_manager: String,
    pub mirrors: Vec<Mirror>,
    pub kernel: String,
    pub init_system: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Mirror {
    pub protocol: String,
    pub count: String,  // e.g., "10-20"
    pub options: Vec<String>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct StorageLayout {
    pub total_disk: String,
    pub compression: String,
    pub partitions: HashMap<String, String>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct NetworkConfig {
    pub lan_inference: bool,
    pub gpu_sharing: bool,
    pub firewall: String,
    pub services: Vec<String>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct SecurityConfig {
    pub sandboxing: String,
    pub root_readonly: bool,
    pub user_isolation: bool,
    pub backup_strategy: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct DevelopmentConfig {
    pub containers: Vec<String>,
    pub kubernetes: String,
    pub vms: Vec<String>,
    pub gpu_passthrough: bool,
    pub lan_gpu_serving: bool,
}

pub fn load_schema(path: &Path) -> anyhow::Result<Project> {
    let content = std::fs::read_to_string(path)?;
    let project: Project = serde_yaml::from_str(&content)?;
    Ok(project)
}