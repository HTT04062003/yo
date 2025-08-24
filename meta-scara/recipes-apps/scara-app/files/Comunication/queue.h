#ifndef QUEUE_H
#define QUEUE_H
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Cấu trúc một Node trong hàng đợi
typedef struct Node {
    uint32_t num;         // Mã số, ID hoặc đánh số thứ tự
    float Y;             // Dữ liệu lưu trong node
    int ID;
    struct Node* next;    // Con trỏ đến node kế tiếp
} Node;

// Cấu trúc hàng đợi
typedef struct {
    Node* front;          // Node đầu hàng (để dequeue)
    Node* rear;           // Node cuối hàng (để enqueue)
} Queue;

void initQueue(Queue* q) ;
int isEmpty(Queue* q);
void enqueue(Queue* q, uint32_t num,  int ID,float Start_Y);
int dequeue(Queue* q, uint32_t* num, int *ID,int* Y);
void updateAllDataWithOffset(Queue* q, float offset) ;
void updateIDByNum(Queue* q, uint32_t targetNum, int newID);
extern Queue item;
extern uint64_t num_of_item;
extern uint64_t item_scanned;
extern uint64_t item_picked;
extern int new_id;
#endif