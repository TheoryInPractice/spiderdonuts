clear; clc; clf;

C = diag( ones(3,1), 1);
C(4,1) = 1;
C = C|C';
B = [ 0, ones(1,4) ; ones(4,1), C ];

A = [ B, eye(5); eye(5), B ];

A(1,6) = 0;
A(6,1) = 0;

G = graph(A,'OmitSelfLoops');
plot(G);

print(gcf, 'walk-counterexample', '-depsc')

%%
n = size(A,1);
Ds = zeros(n,n-1);
Ak = A;
for k=2:n,
    Ak = Ak*A;
	Ds(:,k-1) = diag( Ak );
end


%%
% Nodes 1 and 6 are type a, the rest are type b.
% a-nodes and b-nodes flip flop!

% Here we construct a function of A that has constant diagonal, even though
% this graph is not walk regular.

EA = expm(A);

% subtract terms k = 3 and 4, which correspond to Ds(:,[2,3])
T3 = (1/6)*A^3;
T4 = (1/24)*A^4;

tempEA = EA-T3 - T4;

% There are two kinds of nodes, a nodes and b nodes.
% 1 and 6 are a nodes, the rest are b nodes.
abvals = [ tempEA(1,1), tempEA(2,2) ];
[~,aind] = max(abvals);
[~,bind] = min(abvals);
asum = tempEA(aind,aind);
bsum = tempEA(bind,bind);
dsub = Ds([1,2],[2,3]); % row 1 is a nodes, row 2 is b nodes
% column 1 corresponds to coefficient of A^2, col 2 coresponds to A^3.
k1 = (dsub(bind,1)-dsub(aind,1));
k2 = (dsub(bind,2)-dsub(aind,2));
if k1 < 0,
    alpha = -bsum/k1;
    beta = asum/k2;
else
    alpha = asum/k1;
    beta = -bsum/k2;
end

fA = expm(A) + (alpha - 1/6)*A^3 + (beta - 1/24)*A^4;

diag(fA)
