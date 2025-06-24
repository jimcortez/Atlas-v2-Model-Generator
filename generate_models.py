#!/usr/bin/env python3
"""
Atlas v2 LED Sphere Model Generator

A modular script to generate LED sphere models for various animation software platforms.
Reads configuration from YAML and generates models using the appropriate generators.
"""

import argparse
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

from generators import create_generator, get_available_formats


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML is invalid
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in configuration file: {e}")


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration data.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_sections = ['model', 'rings', 'controller', 'geometry', 'output']
    
    for section in required_sections:
        if section not in config:
            print(f"Error: Missing required configuration section: {section}")
            return False
    
    # Validate rings configuration
    if not config['rings']:
        print("Error: No rings defined in configuration")
        return False
    
    # Validate controller configuration
    if 'ports' not in config['controller']:
        print("Error: Missing 'ports' in controller configuration")
        return False
    
    if 'total_size' not in config['controller']:
        print("Error: Missing 'total_size' in controller configuration")
        return False
    
    return True


def get_enabled_formats(config: Dict[str, Any]) -> List[str]:
    """
    Get list of enabled formats from configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of enabled format names
    """
    enabled_formats = []
    
    if 'output' in config and 'formats' in config['output']:
        for format_name, format_config in config['output']['formats'].items():
            if format_config.get('enabled', False):
                enabled_formats.append(format_name)
    
    return enabled_formats


def generate_models(config: Dict[str, Any], output_dir: str = ".", 
                   formats: Optional[List[str]] = None, prefix: Optional[str] = None) -> bool:
    """
    Generate models for the specified formats.
    
    Args:
        config: Configuration dictionary
        output_dir: Output directory for generated files
        formats: List of formats to generate (if None, uses enabled formats from config)
        prefix: Output filename prefix (if None, uses default from config)
        
    Returns:
        True if all generations were successful, False otherwise
    """
    # Determine which formats to generate
    if formats is None:
        formats = get_enabled_formats(config)
    
    if not formats:
        print("Warning: No formats enabled for generation")
        return False
    
    # Determine output prefix
    if prefix is None:
        prefix = config['output'].get('default_prefix', 'atlas_v2')
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = len(formats)
    
    print(f"Generating LED sphere models for {total_count} format(s): {', '.join(formats)}")
    print(f"Output directory: {output_path.absolute()}")
    print(f"Output prefix: {prefix}")
    print()
    
    for format_name in formats:
        try:
            print(f"Generating {format_name} model...")
            
            # Create generator
            generator = create_generator(format_name, config)
            
            # Generate model
            output_file = output_path / str(prefix)
            success = generator.generate(str(output_file))
            
            if success:
                # Get the actual files that were generated
                file_extensions = []
                if format_name == "xlights":
                    file_extensions = [".xmodel", ".csv", "_coordinates.json"]
                elif format_name == "xlights3d":
                    file_extensions = ["_3d.xmodel", "_3d.csv", "_3d_coordinates.json"]
                elif format_name == "madmapper":
                    file_extensions = [".mmfl"]
                
                generated_files = [f"{prefix}{ext}" for ext in file_extensions]
                print(f"  ✓ Successfully generated {format_name} model files:")
                for file in generated_files:
                    print(f"    - {file}")
                success_count += 1
            else:
                print(f"  ✗ Failed to generate {format_name} model files")
                
        except Exception as e:
            print(f"  ✗ Error generating {format_name} model: {e}")
    
    print()
    if success_count == total_count:
        print(f"✓ Generation completed successfully: {success_count}/{total_count} formats")
        print("  All model files are ready for use in their respective applications.")
    else:
        print(f"⚠ Generation completed with issues: {success_count}/{total_count} formats successful")
        print("  Please check the error messages above for details.")
    
    return success_count == total_count


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate LED sphere models for various animation software platforms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all enabled formats with default settings
  python generate_models.py
  
  # Generate specific formats
  python generate_models.py --formats xlights madrix
  
  # Use custom configuration and output directory
  python generate_models.py --config custom_config.yaml --output-dir ./models
  
  # Use custom output prefix
  python generate_models.py --prefix my_sphere
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default='.',
        help='Output directory for generated files (default: current directory)'
    )
    
    parser.add_argument(
        '--formats', '-f',
        nargs='+',
        choices=get_available_formats(),
        help='Specific formats to generate (default: all enabled formats from config)'
    )
    
    parser.add_argument(
        '--prefix', '-p',
        help='Output filename prefix (default: from config)'
    )
    
    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='List available formats and exit'
    )
    
    args = parser.parse_args()
    
    # List available formats if requested
    if args.list_formats:
        print("Available LED sphere model formats:")
        for format_name in get_available_formats():
            print(f"  - {format_name}")
        return 0
    
    try:
        # Load and validate configuration
        print(f"Loading configuration from: {args.config}")
        config = load_config(args.config)
        
        if not validate_config(config):
            print("Configuration validation failed. Please check your config file.")
            return 1
        
        print("Configuration loaded and validated successfully.")
        print()
        
        # Generate models
        success = generate_models(
            config=config,
            output_dir=args.output_dir,
            formats=args.formats,
            prefix=args.prefix
        )
        
        return 0 if success else 1
        
    except FileNotFoundError:
        print(f"Error: Configuration file '{args.config}' not found.")
        print("Please ensure the file exists or specify a different path with --config.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your configuration and try again.")
        return 1


if __name__ == '__main__':
    sys.exit(main()) 