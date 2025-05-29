import util  # your util.py file

util.load_saved_artifacts()

print(util.__data_columns)  # print columns loaded

# Test prediction with sample input:
price = util.predict_price('1st Phase JP Nagar', 1000, 2, 2)
print(f"Predicted price for sample input: {price}")
