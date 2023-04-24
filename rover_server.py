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

from concurrent import futures
import logging

import grpc
import requests

import rover_pb2
import rover_pb2_grpc

api_url = "REDACTED"

class Rover(rover_pb2_grpc.RoverServicer):
    mines = []

    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = rover_pb2_grpc.RoverStub(self.channel)

        # Init mines file
        with open('mines.txt') as file:
            while (line := file.readline().rstrip()):
                self.mines.append(line.split(' '))


    def GetMap(self, request, context):
        print("GetMap")
        rover_name = request.rover_name
        map = ""

        sizeRead = False
        with open('map.txt') as file:
            while (line := file.readline().rstrip()):
                if sizeRead == False:
                    sizeRead = True
                else:
                    line_split = line.split(' ')
                    for num in line_split:
                        map = map + num + " "
                    map += "\n"
        print(map)
        return rover_pb2.MapResponse(map=map)

    def GetStreamOfCommands(self, request, context):
        print("GetStreamOfCommands")
        rover_index = request.rover_index
        moves_json = requests.get(f'api_url/{rover_index}').json()
        return rover_pb2.MovesResponse(moves=moves_json['data']['moves'])

    def GetMineSerialNumber(self, request, context):
        print("GetMineSerialNumber")
        rover_index = request.rover_index
        # Note: mine coord are in the following format: "y x"
        mine_coord = request.mine_coord
        mine_coord_split = mine_coord.split(" ")
        x = mine_coord_split[1]
        y = mine_coord_split[0]

        mine_serial_num = ""

        for i in range(len(self.mines)):
            if self.mines[i][0] == str(y) and self.mines[i][1] == str(x):
                mine_serial_num = self.mines[i][2]
                break

        # mine_serial_num = "GET MINE SERIAL NUM"
        return rover_pb2.MineSerialNumResponse(rover_index=rover_index, mine_serial_num=mine_serial_num)

    def SayCompletedCommands(self, request, context):
        print("SayCompletedCommands")
        rover_name = request.rover_name
        return rover_pb2.CompletedCommandsResponse(message="Completed commands")

    def ShareMinePin(self, request, context):
        print("ShareMinePin")
        rover_index = request.rover_index
        mine_pin = request.mine_pin
        minePinReceived = "Mine Pin Shared"
        return rover_pb2.ShareMinePinResponse(message=minePinReceived)

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rover_pb2_grpc.add_RoverServicer_to_server(Rover(), server)
    # helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
