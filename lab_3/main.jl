using LinearAlgebra
using IterTools

function sigmoid(x::Real)::Real
	return 1 / (1 + exp(-x))
end

function f(x::AbstractVector{Float64}, w::AbstractVector{Float64}, s::Vector{Float64})::Tuple{Float64, Vector{Float64}}
	dot_product = dot(x, w)
	new_layer = fill(dot_product, size(x))
	println("New Layer (before activation): ", new_layer)
	new_layer = sigmoid.(new_layer .+ s)::Vector{Float64}
	println("New Layer (after activation): ", new_layer)
	s .= new_layer
	final_output = sigmoid(sum(new_layer))
	println("Final Output: ", final_output)
	return final_output, s
end

function chain_f(X::AbstractMatrix, w::AbstractVector, s::AbstractVector)::Tuple{Vector, Vector}
	output = []
	for x in eachrow(X)
    println("\nEvaluating Input: ", x)
		new_output, s = f(x, w, s)
    println("Intermediate State after Input:", s)
		push!(output, new_output)
	end
	return output, s
end


if abspath(PROGRAM_FILE) == @__FILE__
	x_test = [1.0 1.0; 1.0 1.0; 2.0 2.0]
	s_test = [0.0, 0.0]
	w_test = [1.0, 1.0]
	output, final_state = chain_f(x_test, w_test, s_test)

	println("\nFinal Results:", output)
	println("Final State:", final_state)
end
