def scrape_mashable():
    url = "https://sea.mashable.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    seen_titles = set()
    MAX_ARTICLES = 10  # 👈 You can increase this later when it's stable

    # Grab box_title articles
    box_links = soup.find_all("a", class_="box_title")
    for link_tag in box_links:
        if len(headlines) >= MAX_ARTICLES:
            break  # ✅ Stop scraping to prevent timeouts

        title = link_tag.get_text(strip=True)
        if title in seen_titles:
            continue
        seen_titles.add(title)

        relative_link = link_tag['href']
        link = relative_link if relative_link.startswith("http") else f"https://sea.mashable.com{relative_link}"

        pub_date = extract_date_from_article(link)

        if pub_date is None or pub_date >= datetime(2022, 1, 1):
            headlines.append({
                "title": title,
                "link": link,
                "date": pub_date
            })

        time.sleep(1)

    # Grab articles with caption/deck and inline time tag
    all_a_tags = soup.find_all("a")
    for a_tag in all_a_tags:
        if len(headlines) >= MAX_ARTICLES:
            break  # ✅ Again, avoid long scraping

        caption_div = a_tag.find("div", class_="caption")
        time_tag = a_tag.find("time", class_="datepublished")
        if caption_div and time_tag:
            title = caption_div.get_text(strip=True)
            if title in seen_titles:
                continue
            seen_titles.add(title)

            relative_link = a_tag.get("href", "")
            link = relative_link if relative_link.startswith("http") else f"https://sea.mashable.com{relative_link}"

            try:
                pub_date = datetime.strptime(time_tag.text.strip(), "%B %d, %Y")
            except:
                pub_date = None

            if pub_date is None or pub_date >= datetime(2022, 1, 1):
                headlines.append({
                    "title": title,
                    "link": link,
                    "date": pub_date
                })

            time.sleep(1)

    # Sort articles by date, with missing dates at the bottom
    headlines.sort(key=lambda x: x["date"] or datetime.min, reverse=True)
    return headlines
