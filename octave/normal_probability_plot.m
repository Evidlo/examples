## Evan Widloski - 2016-06-25
## A crappy reimplementation of pplot
## Distributions which are normal should appear linear

[nn,xx] = hist(rand(10000,1),100);

rel_freq = nn./sum(nn);

# normal cdf distribution -> linear, delete entries that produce Inf
y = cumsum(rel_freq);

del = [y >= .99999]
xx(del) = [];
y(del) = [];

y = norminv(y);
plot(xx,y);

# add comparison line
hold on
p=polyfit(xx,y,1);
plot(xx,polyval(p,xx),'r');

# calculate labels
yl=get(gca,'YTickLabel')

for i = 1:length(yl)
  yl{i} = sprintf('%f',normcdf(str2num(yl{i})));
end

set(gca,'YTickLabel',yl)
