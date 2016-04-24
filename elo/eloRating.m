
% Initialization
clear ; close all; clc

% Load Data 
data = csvread('../combinedData.csv');
% note - this needs to include team info; 
% need to determine columns so that we can fill in blanks below
teams = csvread('../data/Teams.csv'); 

% Elo variables
n = size(teams(:,[1])); 
m = size(data(:,[1])); 
k = 32; 
year = ? 
ratings = zeros(n); 
for i=1:n
  ratings[i] = 1500; 
end

% calculate elo ratings
for i=1:m
  if data[year] != year 
    year++; 
    for j=1:n
      ratings[j] = .75 * r1 + .25 * 1500; 
    end
  end
  Ra = ratings[?]; 
  Rb = ratings[?]; 
  if homeadvantage 
    Ra OR Rb += 100
  end
  Ea = 1/(1+(10^((Rb-Ra)/400))); 
  Eb = 1/(1+(10^((Ra-Rb)/400))); 
  Sa = data[?]; 
  Sb = data[?]; 
  ratings[?] = Ra + k*(Sa-Ea); 
  ratings[?] = Rb + k*(Sb-Eb); 
end

% apply elo ratings to sample submissions dataset




