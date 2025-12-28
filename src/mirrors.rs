use crate::schema::DebianConfig;
use anyhow::Result;
use reqwest::Client;
use std::collections::HashSet;

pub async fn fetch_mirrors(config: &DebianConfig) -> Result<Vec<String>> {
    let client = Client::new();

    // Fetch mirror list from Debian
    let url = "https://www.debian.org/mirror/mirrors_full";
    let response = client.get(url).send().await?;
    let text = response.text().await?;

    // Parse for HTTPS mirrors
    let mut mirrors = HashSet::new();
    for line in text.lines() {
        if line.contains("https://") && line.contains("debian.org") {
            if let Some(start) = line.find("https://") {
                if let Some(end) = line[start..].find('"') {
                    let mirror = &line[start..start + end];
                    if mirror.ends_with('/') {
                        mirrors.insert(mirror.to_string());
                    }
                }
            }
        }
    }

    // Filter to 6-10 mirrors
    let mut result: Vec<String> = mirrors.into_iter().take(10).collect();
    result.truncate(10.min(result.len()));
    if result.len() < 6 {
        // Fallback to known mirrors
        result = vec![
            "https://deb.debian.org/".to_string(),
            "https://mirror.pit.teraswitch.com/debian/".to_string(),
            "https://mirrors.gigenet.com/debian/".to_string(),
            "https://mirror.us-ny2.kamatera.com/debian/".to_string(),
            "https://nyc.mirrors.clouvider.net/debian/".to_string(),
            "https://mirror.cogentco.com/debian/".to_string(),
        ];
    }

    Ok(result)
}