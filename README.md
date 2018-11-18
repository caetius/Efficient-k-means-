Welcome
--
This code serves to cluster j-subspaces into k clusters in polynomial time.
Please, make sure to pass the correct arguments:
-i data/<input_file.csv> -o data/<output_file.csv> -j 1 -k 2  -alpha alpha -beta -beta


Input
--
The input and output files specified in the params must be relative and of the sort: "data/input.csv", "data/output.csv".
You are responsible to generate your own input. The input file is a csv containing a matrix of size n*(j+1) x d . Each j+1 lines represent the n, d-dimensional subspace inputs. Each subspace consists of j lines representing the subspace's vectors and an additional vector for the displacement. 


Algorithm
--
The algorithm is as described in the paper. There are still many comments relevant for us. 
The algorithm runs Algorithm.py, taking the code for Smart sampling from the Sampler class. 
 

I/O
--
Intermediate files are created and destroyed by the program on every run.