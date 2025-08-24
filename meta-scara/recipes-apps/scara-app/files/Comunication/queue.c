#include "queue.h"
Queue item;
uint64_t num_of_item = 0;
uint64_t item_scanned = 0;
uint64_t item_picked = 0;
int new_id = 0;
// Khởi tạo hàng đợi rỗng
void initQueue(Queue* q) {
    q->front = q->rear = NULL;
}

// Kiểm tra hàng đợi rỗng
int isEmpty(Queue* q) {
    return q->front == NULL;
}

// Thêm phần tử vào hàng đợi
void enqueue(Queue* q, uint32_t num,  int ID,float Start_Y) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) {
        fprintf(stderr, "Lỗi cấp phát bộ nhớ!\n");
        exit(EXIT_FAILURE);
    }
    newNode->num = num;
    newNode->ID = ID;
    newNode->Y = Start_Y;
    newNode->next = NULL;

    if (q->rear == NULL) {
        q->front = q->rear = newNode;
    } else {
        q->rear->next = newNode;
        q->rear = newNode;
    }
}

// Lấy phần tử ra khỏi hàng đợi
int dequeue(Queue* q, uint32_t* num, int *ID,int* Y) {
    if (isEmpty(q)) return -1;

    Node* temp = q->front;
    *num = temp->num;
    *Y = temp->Y;
    *ID = temp->ID; 
    q->front = q->front->next;

    if (q->front == NULL)
        q->rear = NULL;

    free(temp);
    return 0;
}
void updateAllDataWithOffset(Queue* q, float offset) {
    Node* current = q->front;
    while (current != NULL) {
        current->Y += offset;
        current = current->next;
    }
}
void updateIDByNum(Queue* q, uint32_t targetNum, int newID) {
    Node* current = q->front;
    while (current != NULL) {
        if (current->num == targetNum) {
            current->ID = newID;
        }
        current = current->next;
    }
}