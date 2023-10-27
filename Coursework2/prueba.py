def real_to_finite_field(x, prime_modulus):
    # Map a real number x to an element in Z_p
    scaled_x = x * prime_modulus
    integer_x = round(scaled_x) % prime_modulus
    return integer_x

# Example usage with Z_5 as the prime modulus
prime_modulus = 5
real_numbers = [-1, 0.5, 3]

transformed_numbers = [real_to_finite_field(x, prime_modulus) for x in real_numbers]

print("Transformed Numbers in Z_5:", transformed_numbers)