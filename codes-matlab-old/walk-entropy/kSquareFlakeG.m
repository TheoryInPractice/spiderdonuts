function A = kSquareFlakeG(k)
% function A = kSquareFlakeG(k)
%
% generates a graph with a center node connected to k 4-cycles
A = kstarG(k);
A = [ A, zeros(k+1,k) ; zeros(k,k+1), zeros(k) ];

for j=(k+2):(2*k),
    A(j,(j-k)) = 1;
    A(j,(j-k+1)) = 1;
end
    j = (2*k+1);
    A(j,k+1) = 1;
    A(j,2) = 1;
    
    A = A|A';