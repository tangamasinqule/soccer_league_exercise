#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import logging
import click
log = logging.getLogger( __name__ )

@click.command()
@click.option('--input_file', type=click.Path(exists=True), help='The input file with the team name and scores of the league games.')
@click.option('--output_file', type=click.Path(exists=False), help='The output file with each team game statistics.')
def main(input_file, output_file):
    lines = [line.rstrip('\n') for line in open(input_file)]
    team_set = build_team_list(lines)

    league = {}
    for team in team_set:
        league[team] = 0
        for l in lines:
            if team in l:
                league[team] = league[team] + calculate_points(team, l)

    #sort the dictionary by value
    sorted_list = [(k,v) for v,k in sorted(
                 [(v,k) for k,v in league.items()], reverse=True
                 )
              ]
    write_output_file(sorted_list, output_file)

def build_team_list(teams):
    team_list = []
    for t in teams:
        x = t.split(',')
        team_list.append(x[0][:-1].strip())
        team_list.append(x[1][:-1].strip())
    return set(team_list)

def calculate_points(team, score_line):
    scores = score_line.split(',')
    team_score = 0
    opponent_score = 0
    if team in scores[0]:
        team_score = scores[0].rsplit(' ', 1)[1]
        opponent_score = scores[1].rsplit(' ', 1)[1]
    elif team in scores[1]:
        team_score = scores[1].rsplit(' ', 1)[1]
        opponent_score = scores[0].rsplit(' ', 1)[1]

    if int(team_score) > int(opponent_score):
        points = 3
    elif int(team_score) == int(opponent_score):
        points = 1
    else:
        points = 0
    return points

def write_output_file(sorted_list, output_file):
    f = open(output_file,'w')
    for sl in sorted_list:
        line = str(list(sl)[0]) + ", " + str(list(sl)[1]) + " pts"
        f.write(line + '\n') # python will convert \n to os.linesep
    f.close()

if __name__ == '__main__':
    main()

