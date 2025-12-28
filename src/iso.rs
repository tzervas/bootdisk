use anyhow::Result;
use reqwest::Client;
use std::fs;
use std::path::Path;
use std::process::Command;

pub async fn create_custom_iso(preseed_path: &Path, output_iso: &Path) -> Result<()> {
    let client = Client::new();

    // Debian netinst ISO URL (using bullseye as trixie ISO not available)
    let iso_url = "https://deb.debian.org/debian-cd/current/amd64/iso-cd/debian-12.7.0-amd64-netinst.iso";

    // Download ISO
    println!("📥 Downloading Debian ISO...");
    let response = client.get(iso_url).send().await?;
    let iso_bytes = response.bytes().await?;
    let temp_iso = Path::new("temp.iso");
    fs::write(&temp_iso, iso_bytes)?;

    // Extract ISO contents
    let extract_dir = Path::new("iso_extract");
    fs::create_dir_all(&extract_dir)?;
    Command::new("xorriso")
        .args(&["-osirrox", "on", "-indev", temp_iso.to_str().unwrap(), "-extract", "/", extract_dir.to_str().unwrap()])
        .status()?;

    // Copy preseed to isolinux/preseed.cfg or similar
    let preseed_dest = extract_dir.join("preseed.cfg");
    fs::copy(preseed_path, &preseed_dest)?;

    // Create new ISO
    Command::new("xorriso")
        .args(&[
            "-as", "mkisofs",
            "-o", output_iso.to_str().unwrap(),
            "-isohybrid-mbr", "/usr/lib/ISOLINUX/isohdpfx.bin",
            "-c", "isolinux/boot.cat",
            "-b", "isolinux/isolinux.bin",
            "-no-emul-boot",
            "-boot-load-size", "4",
            "-boot-info-table",
            extract_dir.to_str().unwrap(),
        ])
        .status()?;

    // Cleanup
    fs::remove_file(temp_iso)?;
    fs::remove_dir_all(extract_dir)?;

    println!("✅ Custom ISO created at: {:?}", output_iso);
    Ok(())
}