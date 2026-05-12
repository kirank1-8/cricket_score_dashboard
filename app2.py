import streamlit as st
import requests

st.set_page_config(page_title="IPL Live Dashboard", layout="wide")

st.title("🏏 IPL Live Score Dashboard")

# =========================
# API KEYS
# =========================

CRICAPI_KEY = "YOUR_API_ID"

RAPIDAPI_KEY = "YOUR_API_ID"

# =========================
# FUNCTION 1 → CricAPI
# =========================

def get_cricapi_matches():

    url = f"https://api.cricapi.com/v1/currentMatches?apikey={CRICAPI_KEY}&offset=0"

    response = requests.get(url)

    data = response.json()

    matches = []

    if "data" in data:

        for match in data["data"]:

            if "IPL" in match["name"] or "Indian Premier League" in match["name"]:

                matches.append({
                    "source": "CricAPI",
                    "name": match["name"],
                    "status": match["status"],
                    "score": match.get("score", [])
                })

    return matches


# =========================
# FUNCTION 2 → RapidAPI
# =========================

def get_rapidapi_matches():

    url = "https://cricket-api-free-data.p.rapidapi.com/cricket-livescores"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "cricket-api-free-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    matches = []

    if "response" in data:

        for match in data["response"]:

            title = match.get("title", "")

            if "IPL" in title or "Indian Premier League" in title:

                matches.append({
                    "source": "RapidAPI",
                    "name": title,
                    "status": match.get("update", ""),
                    "score": match.get("score", "")
                })

    return matches


# =========================
# FETCH MATCHES
# =========================

all_matches = []

try:
    all_matches.extend(get_cricapi_matches())
except:
    st.warning("CricAPI failed")

try:
    all_matches.extend(get_rapidapi_matches())
except:
    st.warning("RapidAPI failed")


# =========================
# DISPLAY MATCHES
# =========================

if len(all_matches) == 0:

    st.error("No IPL matches found")

else:

    for match in all_matches:

        st.subheader(match["name"])

        st.write("Source:", match["source"])

        st.write("Status:", match["status"])

        if isinstance(match["score"], list):

            for inning in match["score"]:

                st.write(
                    f'{inning["inning"]} - {inning["r"]}/{inning["w"]} ({inning["o"]} overs)'
                )

        else:
            st.write("Score:", match["score"])

        st.markdown("---")
