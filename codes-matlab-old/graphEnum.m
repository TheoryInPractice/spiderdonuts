% Generate all graphs of size N
% Check each graph for particular property.
%
% Successully generated all graphs on N nodes for N= 3, 4, appears to be
% correct, no problems found yet.
%
% Kyle Kloster, NCSU July 2016

N = 4;
edges = zeros( nchoosek(N,2), 2) ;
index = 0;

for a = 1:N,
    for b = (a+1):N
        index = index+1;
        edges(index,:) = [a,b];
    end
end

NUM_EDGES = length(edges);
for which_toggle=1:(2^NUM_EDGES),
    edge_toggles = dec2bin(which_toggle-1);
    NUM_TOGGLES = length(edge_toggles);
    edge_status = zeros(NUM_EDGES,1);
    for which_edge=1:NUM_TOGGLES,
        edge_status(which_edge) = str2num(edge_toggles(which_edge));
    end
    A = sparse( edges(:,1), edges(:,2), edge_status, N,N );
    A = A|A';
    A = full(A);
    %%% CHECK GRAPH PROPERTY HERE
    
    bdiags = zeros(N,N-1);
    Ak = A;
    for k=2:N,
        Ak = Ak*A;
        bdiags(:,k-1) = diag(Ak);
    end
    
    
end