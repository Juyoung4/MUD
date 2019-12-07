from final_KmeansClass import *

main_economy = run_kmeans('economy',15,30)
main_it =run_kmeans('IT_science',10,20)
main_society =run_kmeans('society',15,30)
main_politics =run_kmeans('politics',15,25)

mainlist = [main_economy,main_it,main_society,main_politics]
# main_economy.play()
# main_it.play()
# main_society.play()
# main_politics.play()

from multiprocessing import Process
#유동K가지고 멀티프로세싱 클러스터링
def multi_Clustering_optimalK(mainlist):
    for categorymain in mainlist:
        print('category start')
        proc = Process(categorymain.play())
        proc.start()

#고정K가지고 멀티프로세싱 클러스터링
def multi_Clustering_fixedK(mainlist):
    for categorymain in mainlist:
        proc = Process(categorymain.play_fixK())
        proc.start()




multi_Clustering_optimalK(mainlist)
'6:18분시작'
