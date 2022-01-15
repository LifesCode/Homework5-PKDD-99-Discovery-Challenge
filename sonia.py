import matplotlib.pyplot as plt
# function for plotting histogram.
def histogram(df, col_name, bins):
    plt.hist(df[col_name], alpha=0.5, label=col_name, bins=bins)
    plt.legend(loc='upper right')
    plt.show()



# print(trans_df.head(n=10))
