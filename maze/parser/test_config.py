from config_parser import parse_config, ConfigError


def main():
    config_path = "config.txt"

    try:
        config = parse_config(config_path)

        print("\n✅ CONFIG LOADED SUCCESSFULLY\n")
        print("WIDTH:", config.width)
        print("HEIGHT:", config.height)
        print("ENTRY:", config.entry)
        print("EXIT:", config.exit)
        print("OUTPUT_FILE:", config.output_file)
        print("PERFECT:", config.perfect)
        print("SEED:", config.seed)

    except ConfigError as e:
        print("\n❌ CONFIG ERROR")
        print(e)


if __name__ == "__main__":
    main()
