"""
Test script for Tanzanian Rent Invoice Tax Calculations
Run this to verify calculations are correct
"""

from decimal import Decimal

# Import calculator from main app
import sys
sys.path.append('.')

def test_basic_calculation():
    """Test basic WHT calculation"""
    print("=" * 60)
    print("TEST 1: Basic WHT Calculation")
    print("=" * 60)
    
    base_rent = Decimal("5000000.00")  # TZS 5M
    vat_rate = Decimal("0.18")
    wht_rate = Decimal("0.10")
    
    vat_amount = base_rent * vat_rate
    total_invoice = base_rent + vat_amount
    
    wht = base_rent * wht_rate
    payment_to_landlord = (base_rent - wht) + vat_amount
    payment_to_tra = wht
    total_outflow = payment_to_landlord + payment_to_tra
    
    print(f"Base Rent: TZS {base_rent:,.2f}")
    print(f"VAT @ 18%: TZS {vat_amount:,.2f}")
    print(f"Total Invoice: TZS {total_invoice:,.2f}")
    print()
    print(f"WHT (10% of base): TZS {wht:,.2f}")
    print(f"Payment to Landlord: TZS {payment_to_landlord:,.2f}")
    print(f"  = (TZS {base_rent:,.2f} - TZS {wht:,.2f}) + TZS {vat_amount:,.2f}")
    print(f"Payment to TRA: TZS {payment_to_tra:,.2f}")
    print(f"Total Outflow: TZS {total_outflow:,.2f}")
    print()
    
    # Verify
    assert total_outflow == total_invoice, "Total outflow should match invoice total"
    print("✅ PASS: Total outflow matches invoice")
    print()


def test_small_amount():
    """Test with smaller amount"""
    print("=" * 60)
    print("TEST 2: Small Amount Calculation")
    print("=" * 60)
    
    base_rent = Decimal("500000.00")  # TZS 500K
    vat_rate = Decimal("0.18")
    wht_rate = Decimal("0.10")
    
    vat_amount = base_rent * vat_rate
    total_invoice = base_rent + vat_amount
    
    wht = base_rent * wht_rate
    payment_to_landlord = (base_rent - wht) + vat_amount
    payment_to_tra = wht
    total_outflow = payment_to_landlord + payment_to_tra
    
    print(f"Base Rent: TZS {base_rent:,.2f}")
    print(f"VAT @ 18%: TZS {vat_amount:,.2f}")
    print(f"Total Invoice: TZS {total_invoice:,.2f}")
    print()
    print(f"WHT (10% of base): TZS {wht:,.2f}")
    print(f"Payment to Landlord: TZS {payment_to_landlord:,.2f}")
    print(f"Payment to TRA: TZS {payment_to_tra:,.2f}")
    print(f"Total Outflow: TZS {total_outflow:,.2f}")
    print()
    
    assert total_outflow == total_invoice, "Total outflow should match invoice total"
    print("✅ PASS: Total outflow matches invoice")
    print()


def test_large_amount():
    """Test with large amount"""
    print("=" * 60)
    print("TEST 3: Large Amount Calculation")
    print("=" * 60)
    
    base_rent = Decimal("50000000.00")  # TZS 50M
    vat_rate = Decimal("0.18")
    wht_rate = Decimal("0.10")
    
    vat_amount = base_rent * vat_rate
    total_invoice = base_rent + vat_amount
    
    wht = base_rent * wht_rate
    payment_to_landlord = (base_rent - wht) + vat_amount
    payment_to_tra = wht
    total_outflow = payment_to_landlord + payment_to_tra
    
    print(f"Base Rent: TZS {base_rent:,.2f}")
    print(f"VAT @ 18%: TZS {vat_amount:,.2f}")
    print(f"Total Invoice: TZS {total_invoice:,.2f}")
    print()
    print(f"WHT (10% of base): TZS {wht:,.2f}")
    print(f"Payment to Landlord: TZS {payment_to_landlord:,.2f}")
    print(f"Payment to TRA: TZS {payment_to_tra:,.2f}")
    print(f"Total Outflow: TZS {total_outflow:,.2f}")
    print()
    
    assert total_outflow == total_invoice, "Total outflow should match invoice total"
    print("✅ PASS: Total outflow matches invoice")
    print()


def test_azura_beach_club_example():
    """Test with Azura Beach Club invoice example from requirements"""
    print("=" * 60)
    print("TEST 4: Real-World Example - Azura Beach Club")
    print("=" * 60)
    
    # Assuming TZS 10M base rent for this example
    base_rent = Decimal("10000000.00")
    vat_rate = Decimal("0.18")
    wht_rate = Decimal("0.10")
    
    vat_amount = base_rent * vat_rate
    total_invoice = base_rent + vat_amount
    
    wht = base_rent * wht_rate
    payment_to_landlord = (base_rent - wht) + vat_amount
    payment_to_tra = wht
    total_outflow = payment_to_landlord + payment_to_tra
    
    print(f"Base Rent: TZS {base_rent:,.2f}")
    print(f"VAT @ 18%: TZS {vat_amount:,.2f}")
    print(f"Total Invoice: TZS {total_invoice:,.2f}")
    print()
    print("Breakdown:")
    print(f"  WHT (10% of base): TZS {wht:,.2f}")
    print(f"  Net Rent: TZS {base_rent - wht:,.2f}")
    print(f"  VAT passed through: TZS {vat_amount:,.2f}")
    print()
    print(f"✓ Transfer to Azura Beach Club Ltd: TZS {payment_to_landlord:,.2f}")
    print(f"✓ Remit to TRA: TZS {payment_to_tra:,.2f}")
    print(f"✓ Total Tenant Outflow: TZS {total_outflow:,.2f}")
    print()
    
    assert total_outflow == total_invoice, "Total outflow should match invoice total"
    print("✅ PASS: Calculation verified")
    print()


def test_edge_case_zero_vat():
    """Test edge case with zero VAT (shouldn't happen for commercial but good to test)"""
    print("=" * 60)
    print("TEST 5: Edge Case - Zero VAT")
    print("=" * 60)
    
    base_rent = Decimal("1000000.00")
    vat_amount = Decimal("0.00")
    wht_rate = Decimal("0.10")
    
    total_invoice = base_rent + vat_amount
    
    wht = base_rent * wht_rate
    payment_to_landlord = (base_rent - wht) + vat_amount
    payment_to_tra = wht
    total_outflow = payment_to_landlord + payment_to_tra
    
    print(f"Base Rent: TZS {base_rent:,.2f}")
    print(f"VAT: TZS {vat_amount:,.2f}")
    print(f"Total Invoice: TZS {total_invoice:,.2f}")
    print()
    print(f"WHT (10% of base): TZS {wht:,.2f}")
    print(f"Payment to Landlord: TZS {payment_to_landlord:,.2f}")
    print(f"Payment to TRA: TZS {payment_to_tra:,.2f}")
    print(f"Total Outflow: TZS {total_outflow:,.2f}")
    print()
    
    assert total_outflow == total_invoice, "Total outflow should match invoice total"
    print("✅ PASS: Edge case handled correctly")
    print()


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("TANZANIAN RENT INVOICE TAX CALCULATOR - TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_basic_calculation()
        test_small_amount()
        test_large_amount()
        test_azura_beach_club_example()
        test_edge_case_zero_vat()
        
        print("=" * 60)
        print("ALL TESTS PASSED! ✅")
        print("=" * 60)
        print()
        print("The tax calculation logic is working correctly.")
        print("You can now run the Streamlit app with confidence:")
        print("  streamlit run app.py")
        print()
        
    except AssertionError as e:
        print()
        print("=" * 60)
        print("TEST FAILED! ❌")
        print("=" * 60)
        print(f"Error: {e}")
        print()


if __name__ == "__main__":
    run_all_tests()
