# Analysis Brazilian E-Commerce Dataset by Olist

This is an e-commerce dataset of orders made on Olist Store. The largest department store in the Brazilian marketplace. It contains around 100k order details from 2016 to 2018.

# Environmet Setup with Conda Package Manager 🐍
1. Clone this repostory
```bash
git clone https://github.com/hng011/brazilian-ecommerce-analysis.git <.|folder_name>
```

2. Create a new Conda environment
```bash
conda create -n olist_env python=3.11 -y
```

3. Activating the environment
```bash
conda activate olist_env
```

4. Make sure that you've already in the correct directory, then install packages listed in the requirements.txt file using the following command
```bash
pip install -r requirements.txt
```

5. Start the jupyter-lab
```
jupyter lab
```

# How to run the streamlit app 🤔
1. Go to the `dashboard` folder and ensure that you've already installed all the packages listed in the requirements.txt file
2. Run the following command
```bash
streamlit run dashboard.py
```