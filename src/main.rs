mod schema;
mod preseed;
mod mirrors;
mod iso;

use anyhow::Result;
use std::path::Path;

#[tokio::main]
async fn main() -> Result<()> {
    println!("🚀 Bootdisk - Debian Workstation Setup Automation");
    println!("={}", "=".repeat(50));

    // Load bootdisk schema
    let schema_path = Path::new("bootdisk_schema.yaml");
    if !schema_path.exists() {
        eprintln!("❌ Bootdisk schema not found at: {:?}", schema_path);
        std::process::exit(1);
    }

    println!("📋 Loading schema from: {:?}", schema_path);

    let project = schema::load_schema(schema_path)?;
    println!("✅ Schema loaded successfully: {}", project.project);

    // Create output directory
    let output_dir = Path::new("output");
    std::fs::create_dir_all(output_dir)?;

    // Fetch mirrors
    println!("🌐 Fetching mirrors...");
    let mirrors = mirrors::fetch_mirrors(&project.debian_config).await?;
    println!("✅ Fetched {} mirrors", mirrors.len());

    // Generate preseed
    preseed::generate_preseed(&project, output_dir)?;

    // Create custom ISO
    let preseed_path = output_dir.join("preseed.cfg");
    let iso_path = output_dir.join("bootdisk.iso");
    iso::create_custom_iso(&preseed_path, &iso_path).await?;

    println!("🎯 Bootdisk ISO ready!");
    println!("Next steps:");
    println!("  - Test ISO in VM");
    println!("  - Verify installation");

    Ok(())
}