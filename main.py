#Created main execution file
def main():
    """
    Main execution function for Sales Analytics System
    """

    print("=" * 30)           ## Header
    print("SALES ANALYTICS SYSTEM")       ## Title      

    try:
        # --------------------------------------------------
        # 1. Read sales data
        # --------------------------------------------------
        print("\n[1/10] Reading sales data...")     ## Step info
        sales_data = ("data/sales_data.txt")       ## Input file path
        raw_lines = file_handler.read_sales_data(sales_data, encodings)    ## Read raw data lines
        print(f"Successfully read {len(sales_data)} transactions")    ## Confirmation
    

        # --------------------------------------------------
        # 2. Parse & clean data
        # --------------------------------------------------
        print("\n[2/10] Parsing and cleaning data...")  
        cleaned_data = file_handler.parse_transactions(raw_lines)  ## Parse transactions
        print(f" Parsed {len(cleaned_data)} records")      ## Confirmation
        

        # --------------------------------------------------
        # 3. Show filter options
        # --------------------------------------------------
        print("\n[3/10] Filter Options Available:")
        regions = sorted(set(txn["Region"]         ## Extract unique regions
                         for txn in cleaned_data if txn["Region"]))       ## Non-empty regions
        amounts = [txn["TotalAmount"] for txn in cleaned_data]     ## Extract amounts

        try:
            amounts = [txn["Quantity"] * txn["UnitPrice"]    ## Calculate amounts
                       for txn in cleaned_data]
        except Exception:
            pass

        print(f"Regions: {', '.join(regions)}" if regions else "Regions: None")   ## Display regions
        if amounts:
            print(f"Amount Range: ₹{min(amounts):,} - ₹{max(amounts):,}")   ## Display amount range
        else:
            print("Amount Range: None")     ## No amounts available

        apply_filter = input(
            "\nDo you want to filter data? (y/n): ").strip().lower()    ## User input for filtering

        region = None     ## Initialize filter variables
        min_amt = None    
        max_amt = None

        if apply_filter == "y":     ## If user wants to filter
            region = input("Enter region (or press Enter to skip): ").strip()    ## Region filter input
            min_amt = input(
                "Enter minimum amount (or press Enter to skip): ").strip()  ## Min amount filter input
            try:
                min_amt = float(min_amt) if min_amt else None     ## Convert to float
            except ValueError:
                print("Invalid minimum amount. Skipping this filter.")    ## Handle invalid input

            max_amt = input(
                "Enter maximum amount (or press Enter to skip): ").strip() ## Max amount filter input
            try:
                max_amt = float(max_amt) if max_amt else None
            except ValueError:
                print("Invalid maximum amount. Skipping this filter.") 
               

        # --------------------------------------------------
        # 4. Validate transactions
        # --------------------------------------------------
        print("\n[4/10] Validating transactions...")
        valid_txns, invalid_txn = validate_and_filter(cleaned_data)   ## Validate & filter data
        print(f" Valid: {len(valid_txns)} | Invalid: {len(invalid_txn)}")

        # --------------------------------------------------
        # 5. Analysis
        # --------------------------------------------------
        print("\n[5/10] Analyzing sales data...")
        analysis_results = customer_analysis(valid_txns)    ### Perform customer analysis
        print(" Analysis complete")

        # --------------------------------------------------
        # 6. Fetch product data
        # --------------------------------------------------
        print("\n[6/10] Fetching product data from API...")
        product_data = fetch_all_products()    ## Fetch product data from API
        print(f" Fetched {len(product_data)} products")

        # --------------------------------------------------
        # 7. Enrich data
        # --------------------------------------------------
        print("\n[7/10] Enriching sales data...")
        enriched_data = enrich_sales_data(valid_txns, product_data)      ## Enrich sales data
        success_rate = (len(enriched_data) / len(valid_txns)) * 100      ## Calculate success rate
        print(
            f" Enriched {len(enriched_data)}/{len(valid_txns)} transactions ({success_rate:.1f}%)") ## Display result

        # --------------------------------------------------
        # 8. Save enriched data
        # --------------------------------------------------
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_data, "data/enriched_sales_data.txt")   ## Save enriched data
        print(" Saved to: data/enriched_sales_data.txt")

        # --------------------------------------------------
        # 9. Generate report
        # --------------------------------------------------
        print("\n[9/10] Generating report...")
        generate_sales_report(
            analysis_results, enriched_data, "output/sales_report.txt")    ## Generate sales report
        print(" Report saved to: output/sales_report.txt")

        # --------------------------------------------------
        # 10. Completion
        # --------------------------------------------------
        print("\n[10/10] Process Complete!")
        print("=" * 30)       ## Footer

    except Exception as e:
        print("\n ERROR OCCURRED")   ## Error header
        print("Reason:", str(e))     ## Display error reason
        print("Please check your data or function implementations.")   ## Error handling message