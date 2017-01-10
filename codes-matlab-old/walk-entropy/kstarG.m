function S = kstarG(k)
% function S = kstarG(k)
% Create a k-star graph

S = [ 0, ones(1,k); ones(k,1), zeros(k) ]