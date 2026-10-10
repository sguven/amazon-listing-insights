# Amazon Listing Insights

A Streamlit tool for Amazon sellers. Upload the Seller Central Business Report
*Detail Page Sales and Traffic by Child Item* (CSV or Excel) and it ranks your ASINs
into two lists:

- **Desirable but not discoverable** – shoppers who find these listings buy them, but
  few find them. Good candidates for more advertising.
- **Discoverable but not desirable** – plenty of traffic, few orders. The listing
  itself (price, images, title, reviews) probably needs work.

The ranking uses conversion per page view: `(orders / sessions) / page views`, after
dropping ASINs below a minimum number of sessions so tiny samples don't dominate.

## Run it

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
