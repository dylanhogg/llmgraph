version = "0.2"
output_folder = "./_output/"

# TODO: remove below once migrated:

# COMPANIES --------------------------------------------------------------------------------------------------------------
# company = "Ford Motor Company"
# company = "Tesla Motors"
# company = "O'Reilly Media"
# company = "Penguin Books"
# entity = "Facebook"
# --
# entity_wikipedia = "https://en.wikipedia.org/wiki/Facebook"
# entity_type = "company"
# system = "You are a business executive highly knowledgeable about many international companies."
# prompt_format = (
#     "You are a knowledgeable business executive. "
#     "List, in json array format, the top 5 companies most like '{entity}', "
#     "with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. "
#     "Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. "
#     'Example response: {{"name": "Example company name","wikipedia_link": "https://en.wikipedia.org/wiki/Example_company","reason_for_similarity": "Reason for similarity","similarity": 0.5}}'
# )

# MUSIC --------------------------------------------------------------------------------------------------------------
# entity = "The Rolling Stones"
# entity_type = "music"
# system = "You are a music expert, highly knowledgeable about music, bands and artists."
# prompt_format = (
#     "You are a music expert, highly knowledgeable about music, bands and artists. "
#     "List, in json array format, the top 5 bands or artists most like '{entity}', "
#     "with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. "
#     "Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. "
#     'Example response: {{"name": "Example band or artist name","wikipedia_link": "https://en.wikipedia.org/wiki/Example_band","reason_for_similarity": "Reason for similarity","similarity": 0.5}}'
# )

# LEGAL FIRMS --------------------------------------------------------------------------------------------------------------
# entity = "King & Wood Mallesons"
# entity_type = "legal_firms"
# system = "You are a legal expert and legal partner, highly knowledgeable about legal firms and partnerships."
# prompt_format = (
#     "You are a legal expert and legal partner, highly knowledgeable about legal firms and partnerships. "
#     "List, in json array format, the top 5 legal firms most like '{entity}', "
#     "with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. "
#     "Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. "
#     'Example response: {{"name": "Example legal firm name","wikipedia_link": "https://en.wikipedia.org/wiki/Example_legal_firm","reason_for_similarity": "Reason for similarity","similarity": 0.5}}'
# )

# BOOKS --------------------------------------------------------------------------------------------------------------
# entity = "Pride and Prejudice"
# entity_wikipedia = "https://en.wikipedia.org/wiki/Pride_and_Prejudice"
# entity = "Anna Karenina"
# entity_wikipedia = "https://en.wikipedia.org/wiki/Anna_Karenina"
# entity = "The Very Hungry Caterpillar"
# entity_wikipedia = "https://en.wikipedia.org/wiki/The_Very_Hungry_Caterpillar"
# --
# entity_type = "books"
# system = "You are a book expert, highly knowledgeable about books and authors."
# prompt_format = (
#     "You are a book expert, highly knowledgeable about books and authors. "
#     "List, in json array format, the top 5 book title most like '{entity}', "
#     "with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. "
#     "Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. "
#     'Example response: {{"name": "Example book title","wikipedia_link": "https://en.wikipedia.org/wiki/Example_book_title","reason_for_similarity": "Reason for similarity","similarity": 0.5}}'
# )

# COMPUTER GAME --------------------------------------------------------------------------------------------------------------
# entity = "Thimbleweed Park"
# entity_wikipedia = "https://en.wikipedia.org/wiki/Thimbleweed_Park"
# --
# entity_type = "computer_game"
# system = "You are a knowledgeable computer game player, across many genres and platforms."
# prompt_format = (
#     "You are a knowledgeable computer game player, across many genres and platforms. "
#     "List, in json array format, the top 5 computer games most like '{entity}', "
#     "with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. "
#     "Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. "
#     'Example response: {{"name": "Example computer game name","wikipedia_link": "https://en.wikipedia.org/wiki/Example_computer_game","reason_for_similarity": "Reason for similarity","similarity": 0.5}}'
# )

# PODCAST --------------------------------------------------------------------------------------------------------------
# entity = "Lex Fridman Podcast"
# entity_wikipedia = "https://en.wikipedia.org/wiki/Lex_Fridman"
# entity = "The Rest is History Podcast"
# entity_wikipedia = "https://en.wikipedia.org/wiki/The_Rest_is_History_(podcast)"
# entity = "Sean Carroll's Mindscape Podcast"
# entity_wikipedia = "https://en.wikipedia.org/wiki/Sean_M._Carroll"
# entity = "The Joe Rogan Experience"
# entity_wikipedia = "https://en.wikipedia.org/wiki/The_Joe_Rogan_Experience"
# entity = "Huberman Lab"
# entity = "https://en.wikipedia.org/wiki/Andrew_D._Huberman"
# --
# TODO: note typo in system "You are a knowledgeable about" - fix will clear cache!


# MOVED: TV SHOWS -----------------------------------------------------------------------------------------------------------------------
# entity_type = "tv"
# entity = "Severance"
# entity_wikipedia = "https://en.wikipedia.org/wiki/Severance_(TV_series)"
# entity = "Mr Robot"
# entity_wikipedia = "https://en.wikipedia.org/wiki/Mr._Robot"
# entity = "The Crown"
# entity_wikipedia = "https://en.wikipedia.org/wiki/The_Crown_(TV_series)"
entity = "The Sopranos"
entity_wikipedia = "https://en.wikipedia.org/wiki/The_Sopranos"
# --
# entity_type = "tv"
# system = "You are knowledgeable about TV shows of all types, and genres."
# prompt_format = (
#     "You are knowledgeable about TV shows of all types, and genres. "
#     "List, in json array format, the top 5 TV shows most like '{entity}', "
#     "with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. "
#     "Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. "
#     'Example response: {{"name": "Example TV show name","wikipedia_link": "https://en.wikipedia.org/wiki/Example_TV_Show","reason_for_similarity": "Reason for similarity","similarity": 0.5}}'
# )

# crypto ----------------------------------------------------------------------------------------------------------------
# entity_type = "crypto"
# entity = "Ethereum"
# entity_wikipedia = "https://en.wikipedia.org/wiki/Ethereum"
# --
# entity_type = "crypto"
# system = "You are knowledgeable about cryptocurrencies, digital currencies, blockchain, NFTs, DAOs and distributed finance."
# prompt_format = (
#     "You are knowledgeable about cryptocurrencies, digital currencies, blockchain, NFTs, DAOs and distributed finance. "
#     "List, in json array format, the top 5 cryptocurrencies most like '{entity}', "
#     "with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. "
#     "Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. "
#     'Example response: {{"name": "Example cryptocurrencies name","wikipedia_link": "https://en.wikipedia.org/wiki/Example_cryptocurrency","reason_for_similarity": "Reason for similarity","similarity": 0.5}}'
# )


# -----------------------------------------------------------------------------------------------------------------------
