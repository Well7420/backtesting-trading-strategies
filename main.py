from data_loader import DataLoader


def main():
    loader = DataLoader("2025-02-01", "2025-02-28")
    pairs = loader.get_top_pairs(100)  # 100 пар
    data = loader.load_all_data(pairs)
    print(f"Loaded data for {len(data)} pairs.")


if __name__ == "__main__":
    main()
