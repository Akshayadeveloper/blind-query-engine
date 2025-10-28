
from typing import Callable

# --- Mock Encryption/Decryption Functions ---
# In a real system, these would use FHE/SHE/PHE algorithms
def encrypt(value: int) -> int:
    """Mock encryption: adds a simple large offset."""
    return value + 999999

def decrypt(value: int) -> int:
    """Mock decryption: subtracts the offset."""
    return value - 999999

# --- The Core BlindQuery Engine Class ---
class EncryptedValue:
    """
    Represents a value that can only be operated on while encrypted.
    This mimics the structure needed for Homomorphic Encryption.
    """
    def __init__(self, encrypted_data: int):
        self.encrypted_data = encrypted_data

    @staticmethod
    def _homomorphic_add(a: int, b: int) -> int:
        """Homomorphic Addition: The sum of two encrypted values is the encrypted sum."""
        # In this mock, it's a simple sum, but in FHE, it involves polynomial operations.
        return a + b
    
    @staticmethod
    def _homomorphic_mul(a: int, b: int) -> int:
        """Homomorphic Multiplication: The product of two encrypted values is the encrypted product."""
        # This is the hardest operation in FHE and is heavily constrained.
        # Here we mock it as a required operation on the encrypted value.
        # NOTE: This mock multiplication is NOT cryptographically correct for FHE, 
        # but serves to demonstrate the concept of operating on the object.
        return a * b  

    def __add__(self, other: 'EncryptedValue') -> 'EncryptedValue':
        """Enables addition operation on the encrypted objects."""
        new_encrypted_data = EncryptedValue._homomorphic_add(
            self.encrypted_data, 
            other.encrypted_data
        )
        return EncryptedValue(new_encrypted_data)

    def __mul__(self, other: 'EncryptedValue') -> 'EncryptedValue':
        """Enables multiplication operation on the encrypted objects."""
        new_encrypted_data = EncryptedValue._homomorphic_mul(
            self.encrypted_data, 
            other.encrypted_data
        )
        return EncryptedValue(new_encrypted_data)


# --- Demonstration ---

# 1. Setup: Data is Encrypted by the client before storage
A_clear = 50
B_clear = 10
E_A = EncryptedValue(encrypt(A_clear))
E_B = EncryptedValue(encrypt(B_clear))

print(f"Clear A: {A_clear}, Clear B: {B_clear}")
print(f"Encrypted A: {E_A.encrypted_data}, Encrypted B: {E_B.encrypted_data}")

# 2. Blind Query: The server performs a complex computation (A * 2 + B)
# The server NEVER sees the clear data.
E_A_doubled = E_A * EncryptedValue(encrypt(2)) # A * 2
E_Result = E_A_doubled + E_B                   # (A*2) + B

print("\n--- Computation performed on Encrypted Data ---")
print(f"Encrypted Result: {E_Result.encrypted_data}")

# 3. Decryption: The final result is sent back to the client for decryption
final_clear_result = decrypt(E_Result.encrypted_data)
expected_result = (A_clear * 2) + B_clear

print("\n--- Client Decryption ---")
print(f"Decrypted Result: {final_clear_result}")
print(f"Expected Result: {expected_result}")
print(f"Match: {final_clear_result == expected_result}")
      
