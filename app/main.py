from app.ingestion.text_loader import load_text


def main():
    document = load_text("data/sample_document.txt")

    print("Document text:")
    print(document.text)

    print("\nMetadata:")
    print(document.metadata)


if __name__ == "__main__":
    main()