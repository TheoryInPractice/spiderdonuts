% Constructs the chamfered dodecahedron
% thanks to his website for the ace info:
% http://dmccooey.com/polyhedra/ChamferedDodecahedron3.txt
% http://dmccooey.com/polyhedra/ChamferedDodecahedron3.html

faces = {...
{ 72, 36, 64,  4, 20, 44 },
{ 72, 44, 68,  8, 28, 52 },
{ 72, 52, 60,  0, 12, 36 },
{ 73, 37, 13,  1, 61, 53 },
{ 73, 53, 29,  8, 68, 45 },
{ 73, 45, 21,  5, 65, 37 },
{ 74, 38, 14,  2, 62, 54 },
{ 74, 54, 30,  9, 69, 46 },
{ 74, 46, 22,  4, 64, 38 },
{ 75, 39, 65,  5, 23, 47 },
{ 75, 47, 69,  9, 31, 55 },
{ 75, 55, 63,  3, 15, 39 },
{ 76, 40, 16,  0, 60, 56 },
{ 76, 56, 32, 10, 70, 48 },
{ 76, 48, 24,  6, 66, 40 },
{ 77, 41, 67,  7, 25, 49 },
{ 77, 49, 70, 10, 33, 57 },
{ 77, 57, 61,  1, 17, 41 },
{ 78, 42, 66,  6, 26, 50 },
{ 78, 50, 71, 11, 34, 58 },
{ 78, 58, 62,  2, 18, 42 },
{ 79, 43, 19,  3, 63, 59 },
{ 79, 59, 35, 11, 71, 51 },
{ 79, 51, 27,  7, 67, 43 },
{  2, 14, 12,  0, 16, 18 },
{  3, 19, 17,  1, 13, 15 },
{  4, 22, 23,  5, 21, 20 },
{  7, 27, 26,  6, 24, 25 },
{  8, 29, 33, 10, 32, 28 },
{  9, 30, 34, 11, 35, 31 },
{ 60, 52, 28, 32, 56 },
{ 61, 57, 33, 29, 53 },
{ 62, 58, 34, 30, 54 },
{ 63, 55, 31, 35, 59 },
{ 64, 36, 12, 14, 38 },
{ 65, 39, 15, 13, 37 },
{ 66, 42, 18, 16, 40 },
{ 67, 41, 17, 19, 43 },
{ 68, 44, 20, 21, 45 },
{ 69, 47, 23, 22, 46 },
{ 70, 49, 25, 24, 48 },
{ 71, 50, 26, 27, 51 } };

% Iterate over each face:
%   add each edge from that face to the edge list
edges = [];
for which_face=1:length(faces),
    face = faces{which_face};
    for elem=1:length(face)-1,
        edge = [ face{elem}, face{elem+1} ];
        edges = [edges; edge];
    end
    edges = [edges; [ face{length(face)}, face{1} ] ];
end
edges = edges+1;24
A = sparse( [edges(:,1); edges(:,2)], [edges(:,2);edges(:,1)] , 1 );

% Graph generated!
A = A|A';
A = full(double(A));
G = graph(A,'OmitSelfLoops');
plot(G);


print(gcf, 'chamfered-dodecahedron', '-depsc')
%%
% Here we construct a function of A that has constant diagonal, even though
% this graph is not walk regular.

EA = expm(A);

% By simple inspection, exp(A) proves this graph is not walk regular.
diagEA = diag(EA)
[~,aind] = max(diagEA);
[~,bind] = min(diagEA);
% aind and bind are nodes from the two different classes of node.

% Inspection shows a-nodes and b-nodes "flip-flop" on 5-walks and 6-walks
A5 = A^5;
A6 = A^6;
T5 = (1/120)*A5;
T6 = (1/720)*A6;

% Subract from exp(A) two of the terms where a- and b-nodes flip-flop.
tempEA = EA-T5 - T6;


% There are two kinds of nodes, a nodes and b nodes.
asum = tempEA(aind,aind);
bsum = tempEA(bind,bind);

diagA5 = diag(A5);
diagA6 = diag(A6);

dsub = [ diagA5([aind,bind]) , diagA6([aind,bind]) ];
% rows contain diag info for a-nodes and b-nodes
% column 1 corresponds to coefficient of A^5, col 2 corresponds to A^6.
k1 = (dsub(2,1)-dsub(1,1));
k2 = (dsub(2,2)-dsub(1,2));
if k1 < 0,
    alpha = -bsum/k1;
    beta = asum/k2;
else
    alpha = asum/k1;
    beta = -bsum/k2;
end

% Finally we have our positive coefficients -- now construct a function
% with all positive coefficients
% such tha f(A) has constant diagonal:

fA = expm(A) + (alpha - 1/120)*A5 + (beta - 1/720)*A6;

diagfA = diag(fA);
diagfA

fprintf( 'diag(f(A)) is constant iff this is zero:  %f \n', max( abs( diagfA - ones( size(diagfA) ).*diagfA(1) ) ) );