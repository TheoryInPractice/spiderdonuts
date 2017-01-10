function C = kcycleG(k)
% function C = kcycleG(k)
% Create a k-cycle graph

C = diag( ones(k-1,1), 1 );
C(1,k)=1;
C = double(C|C');