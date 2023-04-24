# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import hashlib
import string
from copy import deepcopy
import random

import grpc

import rover_pb2
import rover_pb2_grpc


class RoverClient(object):
    map = []
    traversed_map = []
    moves = ""

    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = rover_pb2_grpc.RoverStub(self.channel)

    def get_map(self, rover_name):
        print("Getting map from server")
        request = rover_pb2.MapRequest(rover_name=rover_name)
        response = self.stub.GetMap(request)
        map = response.map
        map_arr = []
        # convert string map into individual string values
        map_rows = response.map.split("\n")
        for map_row in map_rows:
            map_row_split = map_row.split(" ")
            if len(map_row_split) > 1:
                map_arr.append(map_row_split[:-1])
        print(map_arr)
        self.map = map_arr

    def get_stream_of_commands(self, rover_index):
        print("Getting stream of commands from server")
        request = rover_pb2.MovesRequest(rover_index=rover_index)
        response = self.stub.GetStreamOfCommands(request)
        print(f"Moves received: {response.moves}")
        self.moves = response.moves
        self.traversed_map = \
            calculate_rover_path(index=rover_index, rover_map=self.map, moves=response.moves, rover_client=self)
        self.executed_all_commands(rover_index=rover_index)

    # mine_coord format will be = "y x"
    def get_mine_serial_num(self, rover_index, mine_coord):
        print("Getting mine serial num from server")
        request = rover_pb2.MineSerialNumRequest(rover_index=rover_index, mine_coord=mine_coord)
        response = self.stub.GetMineSerialNumber(request)
        print("Retrieved mine serial num: " + response.mine_serial_num)
        mine_coord_split = mine_coord.split(" ")
        x = mine_coord_split[1]
        y = mine_coord_split[0]
        hashed_mine_key = disarm_mine(mine_serial_num=response.mine_serial_num, y=y, x=x)
        self.share_mine_PIN_with_server(rover_index=rover_index, mine_pin=hashed_mine_key)

    def executed_all_commands(self, rover_index):
        print("Executed all commands")
        request = rover_pb2.CompletedCommandsRequest(rover_index=rover_index)
        response = self.stub.SayCompletedCommands(request)
        print(response.message)

    def share_mine_PIN_with_server(self, rover_index, mine_pin):
        print("Sharing mine pin with server")
        request = rover_pb2.ShareMinePinRequest(rover_index=rover_index, mine_pin=mine_pin)
        response = self.stub.ShareMinePin(request)
        print(response.message)

def calculate_rover_path(index, rover_map, moves, rover_client):
    print("Calculating rover path")
    moves_arr = deepcopy(rover_map)

    curr_x = 0
    curr_y = 0
    moves_arr[curr_y][curr_x] = '*'

    north = 0
    south = 1
    east = 0
    west = 0
    hit_mine = False
    dug = False
    for move in moves:
        if move == 'M':
            if int(rover_map[curr_y][curr_x]) == 1 and not dug:
                hit_mine = True
                break
            if north == 1:
                if curr_y > 0:
                    curr_y -= 1
            elif south == 1:
                if curr_y < (len(moves_arr[0]) - 1):
                    curr_y += 1
            elif east == 1:
                if curr_x < (len(moves_arr[0]) - 1):
                    curr_x += 1
            elif west == 1:
                if curr_x > 0:
                    curr_x -= 1
            moves_arr[curr_y][curr_x] = '*'
        elif move == 'R':
            # rotate right
            if north == 1:
                east = 1
                north = 0
            elif south == 1:
                west = 1
                south = 0
            elif east == 1:
                south = 1
                east = 0
            elif west == 1:
                north = 1
                west = 0
        elif move == 'L':
            # rotate left
            if north == 1:
                west = 1
                north = 0
            elif south == 1:
                east = 1
                south = 0
            elif east == 1:
                north = 1
                east = 0
            elif west == 1:
                south = 1
                west = 0
        elif move == 'D':
            if int(rover_map[curr_y][curr_x]) == 1:
                print("hit mine...disarming")
                rover_client.get_mine_serial_num(rover_index=index, mine_coord=f"{curr_y} {curr_x}")
                dug = True

        if north == 1:
            curr_dir = "north"
        elif south == 1:
            curr_dir = "south"
        elif east == 1:
            curr_dir = "east"
        elif west == 1:
            curr_dir = "west"
        # print(move + ', ' + curr_dir + ', [' + str(curr_y) + ', ' + str(curr_x) + '], ' + (str(moves_arr[curr_y][curr_x]
        #                                                                                        )))
        # printMap(moves_arr)
    if hit_mine:
        print("ROVER HIT THE MINE")
    # print("final moves map")
    # printMap(moves_arr)
    writePathToFile(index, moves_arr)

    return moves_arr


def writePathToFile(index, path):
    f = open('path_' + str(index) + '.txt', 'w')

    # convert path to string
    for i in range(0, len(path[0])):
        line_str = ''
        for j in range(0, len(path)):
            line_str += str(path[i][j]) + ' '
        f.write(line_str + "\n")
    f.close()


def disarm_mine(mine_serial_num, y, x):
    # Deploy threads and determine the hash value
    #   if thread succeeds, then stop all threads and return the method
    print("Disarming mine")
    pinValid = False
    hashed_mine_key = "UNASSIGNED"

    if mine_serial_num == '':
        print("Error, mine not found")

    while not pinValid:
        pin = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        temporary_mine_key = str(pin) + mine_serial_num
        # print('attempted mine key: ' + temporary_mine_key)
        hashed_mine_key = hashlib.shake_128(temporary_mine_key.encode('utf-8')).hexdigest(3)
        # print('hashed mine key: ' + hashed_mine_key)
        # print(hashed_mine_key[:3])
        if len(hashed_mine_key) < 6:
            print('Error: hashed mine key length is less than 6')
            break
        if str(hashed_mine_key[:6]) == '000000':
            print('hashed mine key: ' + hashed_mine_key)
            pinValid = True
    return hashed_mine_key

def printMap(moves):
    for i in range(0, len(moves[0])):
        for j in range(0, len(moves)):
            print(str(moves[i][j]) + ' ', end='')
        print('')

if __name__ == "__main__":
    client = RoverClient()
    print(client.get_map("rover_name"))
    print(client.get_stream_of_commands("1"))
    # print(client.get_mine_serial_num("1", "1 0"))
    # print(client.share_mine_PIN_with_server("rover_name", "min_pin"))
