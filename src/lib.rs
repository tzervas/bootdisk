pub mod schema;
pub mod preseed;
pub mod mirrors;
pub mod iso;

#[cfg(test)]
mod tests {
    use crate::*;
    use std::path::Path;

    #[test]
    fn test_schema_loading() {
        let schema_path = Path::new("bootdisk_schema.yaml");
        let result = schema::load_schema(schema_path);
        assert!(result.is_ok());
        let project = result.unwrap();
        assert_eq!(project.project, "bootdisk-workstation");
        assert_eq!(project.debian_config.version, "13");
    }

    #[test]
    fn test_preseed_generation() {
        let schema_path = Path::new("bootdisk_schema.yaml");
        let project = schema::load_schema(schema_path).unwrap();
        let output_dir = Path::new("output");
        let result = preseed::generate_preseed(&project, output_dir);
        assert!(result.is_ok());
        let preseed_path = output_dir.join("preseed.cfg");
        assert!(preseed_path.exists());
        let content = std::fs::read_to_string(preseed_path).unwrap();
        assert!(content.contains("trixie"));
        assert!(content.contains("btrfs"));
        assert!(content.contains("zstd"));
    }

    #[tokio::test]
    async fn test_mirror_fetching() {
        let schema_path = Path::new("bootdisk_schema.yaml");
        let project = schema::load_schema(schema_path).unwrap();
        let result = mirrors::fetch_mirrors(&project.debian_config).await;
        assert!(result.is_ok());
        let mirrors = result.unwrap();
        assert!(mirrors.len() >= 6);
        for mirror in mirrors {
            assert!(mirror.starts_with("https://"));
        }
    }
}