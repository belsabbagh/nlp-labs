using Pkg
Pkg.add("JSON")
Pkg.add("Languages")
using JSON
using Languages

# Define English stopwords
const STOPWORDS = stopwords(Languages.English())

# Function to split text into words
function split_into_words(text::String)::Vector{String}
    return split(text, r"\s+")
end

# Function to split text into sentences
function split_into_sentences(text::String)::Vector{String}
    return split(text, r"[.!?]\s*")
end

# Function to parse text
function parse_text(text::String)::Dict{String, Any}
    # Lowercase the text
    text = lowercase(text)
    
    # Tokenize into words
    words = split_into_words(text)
    
    # Filter out stopwords
    filtered_words = filter(w -> !(w in STOPWORDS), words)
    
    # Tokenize into sentences
    sentences = split_into_sentences(text)
    
    # Calculate word frequencies
    word_freqs = Dict{String, Int}()
    for word in filtered_words
        word_freqs[word] = get(word_freqs, word, 0) + 1
    end
    
    # Sort word frequencies
    sorted_word_freqs = sort(collect(word_freqs), by = tuple -> last(tuple), rev = true)
    
    # Return parsed information
    return Dict(
        "clean_text" => join(sentences, " "),
        "most_common_words" => Dict(sorted_word_freqs[1:min(10, length(sorted_word_freqs))]),
        "sentences" => sentences,
        "word_freqs" => word_freqs
    )
end

# Main block
if abspath(PROGRAM_FILE) == @__FILE__
    output = Dict()
    text = read("data/sample.md", String)
    output = parse_text(text)

    open("out/output.json", "w") do f
        JSON.print(f, output, 2)
    end
    println("Output written to output.json")
end
