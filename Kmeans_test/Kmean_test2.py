# coding: utf-8

from __future__ import division
from linear_algebra import squared_distance, vector_mean
import random


class KMeans:
    def __init__(self, k):
        self.k = k # 클러스터의 갯수
        self.means = None # 클러스터의 평균들

    # input 값이 3개의 means 중 어디와 가장 가까운지 찾아서 0,1,2 중 하나를 리턴
    def classify(self, input):
        return min(range(self.k),
        key=lambda i: squared_distance(input, self.means[i]))

    def train(self, inputs):

        self.means = random.sample(inputs, self.k)
        assignments = None

        while True:
            # 요소들이 어느 (변경된)중심점에 가까이 있는지 매핑 [1,1,0,2,1, ... 이런식
            new_assignments = map(self.classify, inputs)

            # 기존 매핑과 동일하다면 더 이상 프로세싱 할 필요 없음. 리턴 ~
            if assignments == new_assignments:
                return

            # 현재 매핑을 저장
            assignments = new_assignments

            # 현재 클러스터링의 중심점 재 계산
            for i in range(self.k):
                i_points = [p for p, a in zip(inputs, assignments) if a == i] # i 번 요소들의 리스트
                if i_points:
                    self.means[i] = vector_mean(i_points) # 그것들의 평균 ( 중심점 )




if __name__ == "__main__":

    inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]

    random.seed(0) # so you get the same results as me
    clusterer = KMeans(3)
    clusterer.train(inputs)
    print ("3-means:")
    print (clusterer.means)
    print ()