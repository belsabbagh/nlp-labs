using Pkg

Pkg.add("Flux")
Pkg.add("CSV")
Pkg.add("DataFrames")
Pkg.add("Statistics")
Pkg.add("WordTokenizers")

using Flux
using Flux.Data: DataLoader
using Flux: onehotbatch, binarycrossentropy, throttle
using WordTokenizers
using CSV
using DataFrames
using Statistics: mean

# Define the RNN model
function rnn_model(vocab_size, embedding_dim, hidden_dim)
    return Chain(
        Flux.Embedding(vocab_size => embedding_dim),
        Flux.LSTM(embedding_dim, hidden_dim),
        Flux.Dense(hidden_dim, 1, σ)
    )
end

function preprocess_sentences(df::DataFrame)
  function tokenize_sentences(df::DataFrame)
      sentences = df[!, :sentence]
      tokenized_sentences = [split(sentence) for sentence in sentences]
      return tokenized_sentences
  end

  function vectorize_sentences(tokenized_sentences, vocab)
      vocab_dict = Dict(word => i for (i, word) in enumerate(vocab))
      vectorized_sentences = [[get(vocab_dict, word, 0) for word in sentence] for sentence in tokenized_sentences]
      return vectorized_sentences
  end

  function pad_sequences(vectorized_sentences)
      maxlen = maximum(length(sentence) for sentence in vectorized_sentences)
      padded_sentences = [vcat(sentence, fill(0, maxlen - length(sentence))) for sentence in vectorized_sentences]
      return padded_sentences
  end

  # Tokenize sentences
  tokenized_sentences = tokenize_sentences(df)

  # Create vocabulary
  vocab = Set(vcat(tokenized_sentences...))

  # Vectorize sentences
  vectorized_sentences = vectorize_sentences(tokenized_sentences, vocab)

  # Pad sequences
  padded_sentences = pad_sequences(vectorized_sentences)

  return padded_sentences, df[!,:label]
end

if abspath(PROGRAM_FILE) == @__FILE__
	# Read data
	df = CSV.read("data/yelp.csv", DataFrame)

	# Preprocess data using WordTokenizers
	padded_sequences, labels = preprocess_sentences(df)
	# Model parameters
	embedding_dim = 16
	vocab_size = length(unique(vcat(padded_sequences...)))
	hidden_dim = 32

	# Define and build the model
	model = rnn_model(vocab_size, embedding_dim, hidden_dim)

	# Define loss function and optimizer
	loss(x, y) = Flux.binarycrossentropy(model(x), y)
	optimizer = Flux.ADAM()

	# Training
	dataset = [(padded_sequences[i], labels[i]) for i in eachindex(labels)]
	evalcb() = @show(mean(loss(padded_sequences[i], labels[i]) for i in eachindex(labels)))
	for epoch in 1:10
		Flux.train!(loss, Flux.params(model), dataset, optimizer, cb = throttle(evalcb, 10))
	end
	# Evaluation
	test_loss = mean(loss(padded_sequences[i], labels[i]) for i in eachindex(labels))
	println("Test Loss: ", test_loss)
end
