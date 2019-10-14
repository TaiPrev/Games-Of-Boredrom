#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <malloc.h>
#include <stdbool.h>
#include <iostream>
using namespace std;

double tablero[16];
double score;

struct node
{
	double data;
	struct node *next;
};

class linked_list
{
	private:
		node *head, *tail;

		double update_sub(node *current)
	 	{	//NOT FULLY WORKING, SECOND POSSITION DOESN'T ADD ONTO THE NEXT
	 		if (current == NULL)
	 		{
	 			return 0;
	 		}
	 		node *second = current->next;
	 		double addition = 0;

	 		if (second == NULL)
	 		{
	 			return 0;
	 		}
	 		cout << "CURRENT VALUE IS: " << current->data << " MEXT VALUE IS: " << second->data << "\n";
	 		if (second->data == current->data)
			{
				current->data += current->data;
				second = second->next;
				current->next = second;
				addition = current->data;
			}

			return addition + update_sub(second);
	 	}
	public:
		linked_list()
		{
			head = NULL;
			tail = NULL;
		}

		void add_node(int n)
		{
			node *tmp = new node;
			tmp->data = n;
			tmp->next = NULL;

			if (head == NULL)
			{
				head = tmp;
				tail = tmp;
			}
			else
			{
				tail->next = tmp;
				tail = tail->next;
			}
		}

		void print_list()
		{	
			node *temp=new node;
    		temp=head;
    		while(temp!=NULL)
    		{
      			cout<<temp->data<<"\t";
    		 	temp=temp->next;
    		}
    		cout << "\n";
		}

		node get_head()
		{
			return *head;
		}

		double update()
		{	
			if (head == NULL)
			{
				return 0;
			}
			node *current;
			node *second = head->next;
			double addition = 0;

			if (second == NULL)
			{
				return 0;
			}

			if (second->data == head->data)
			{
				head->data += head->data;
				second = second->next;
				addition += head->data;
			}
			current = second;
			head->next = current;
			while (current != NULL)
			{
				second = second->next;
				if (second != NULL)
				{
					if (second->data == current->data)
					{
						current->data += current->data;
						second = second->next;
						current->next = second;
						addition += current->data;
					}

					if (second == NULL)
					{
						tail = current;
					}
				}
				current = second;
			}
			return addition;
		}

		double* get_array_double()
		{
			double* res = new double[4];
			node *current = head;
			for (int i=0; i<4; i++)
			{
				if (current==NULL)
				{
					res[i] = 0.0;
				}
				else
				{
					res[i] = current->data;
					current = current->next;
				}
			}
			return res;
		}
};


double* sum_up(double n[4])
{
	linked_list k;
	for (int i=0; i<4; i++)
	{	
		if (n[i]!=0)
		{
			k.add_node(n[i]);
		}
	}
	//k.print_list();

	score += k.update();
	return k.get_array_double();
}

bool is_tablero_full()
{
	for (int i=0; i<16; i++)
	{
		if (tablero[i]==0)
		{
			return false;
		}
	}
	return true;
}

void add_new_value()
{
	srand(time(0));
	int r1 = (rand() % 16);

	while (tablero[r1]!=0){
		r1 = (rand() % 16);
	}
	tablero[r1] = (rand()%2+1)*2;
}

bool movement(int type)
{
	//MAYBE ADD HERE THE NO MOVEMENT DETECTION
	//AND CHANGE THE OUTPUT TO A BOOL
	bool same_state = true;
	if (type == 0) //MOVE UP
	{
		for (int i=0; i<4; i++)
		{
			double n[4] = {tablero[i], tablero[i+4], tablero[i+8], tablero[i+12]};
			double* o = sum_up(n);
			for (int j=0; j<4; j++)
			{
				tablero[i+(j*4)] = o[j];
				if (n[j] != o[j])
				{
					same_state = false;
				}
			}
		}
	}
	else if (type == 1) //MOVE LEFT
	{
		for (int i=0; i<4; i++)
		{
			double n[4] = {tablero[i*4], tablero[i*4+1], tablero[i*4+2], tablero[i*4+3]};
			double* o = sum_up(n);
			for (int j=0; j<4; j++)
			{
				tablero[i*4+j] = o[j];
				if (n[j] != o[j])
				{
					same_state = false;
				}
			}	
		}
	}
	else if (type == 2) //MOVE DOWN
	{
		for (int i=0; i<4; i++)
		{
			double n[4] = {tablero[i+12], tablero[i+8], tablero[i+4], tablero[i]};
			double* o = sum_up(n);
			int k = 0;
			for (int j=3; j>-1; j--)
			{
				tablero[i+(j*4)] = o[k];
				if (n[k] != o[k])
				{
					same_state = false;
				}
				k++;
			}
		}
	}
	else if (type == 3) //MOVE RIGHT
	{
		for (int i=0; i<4; i++)
		{
			double n[4] = {tablero[i*4+3], tablero[i*4+2], tablero[i*4+1], tablero[i*4]};
			double* o = sum_up(n);
			int k = 0;
			for (int j=3; j>-1; j--)
			{
				tablero[i*4+j] = o[k];
				if (n[k] != o[k])
				{
					same_state = false;
				}
				k++;
			}	
		}
	}

	return same_state;
}

void reset_tablero()
{
	srand(time(0));
	int r1 = (rand() % 16);
	int r2 = (rand() % 16);
	while (r2==r1){
		r2 = (rand() % 16);
	}

	cout << r1 << " " << r2 << "\n";

	for (int i=0; i< 16; i++)
	{
		if ((i == r1) || (i == r2))
		{
			tablero[i] = (rand()%2+1)*2;
		}
		else
		{
			tablero[i] = 0;
		}
	}
	score = 0;
}

void init ()
{
	reset_tablero();
	cout << "TABLERO RESETADO \n";
}


void print ()
{
	cout << "SCORE = " << score <<"\n";
	cout << tablero[0] << " ; " << tablero[1] << " ; " << tablero[2] << " ; " << tablero [3] << " ;\n";
	cout << tablero[4] << " ; " << tablero[5] << " ; " << tablero[6] << " ; " << tablero [7] << " ;\n";
	cout << tablero[8] << " ; " << tablero[9] << " ; " << tablero[10] << " ; " << tablero [11] << " ;\n"; 
	cout << tablero[12] << " ; " << tablero[13] << " ; " << tablero[14] << " ; " << tablero [15] << " ;\n"; 
}

void game_loop()
{
	init();
	bool playing = true;
	while (playing)
	{
		print();
		string answer;
		cin >> answer;
		bool same_state_check = true;
		if (answer == "W" || answer == "w")
		{
			same_state_check = movement(0);
		}
		else if (answer == "A" || answer == "a")
		{
			same_state_check = movement(1);
		}
		else if (answer == "S" || answer == "s")
		{
			same_state_check = movement(2);
		}
		else if (answer == "D" || answer == "d")
		{
			same_state_check = movement(3);
		}
		else if (answer == "R" || answer == "r")
		{
			cout << "YOUR FINAL SCORE IS: " << score << "\n";
			init();
		}
		else
		{
			playing = false;
		}

		if (!is_tablero_full())
		{
			if (!same_state_check)
			{
				add_new_value();
			}
		}
		else
		{
			playing = false;
		}
	}
	cout << "YOUR FINAL SCORE IS: " << score << "\n";
}

int main (int argc, char **argv)
{
	cout << "INPUT WASD TO MOVE, R TO RESET \n";
	bool condition = true;
	while(condition){
		game_loop();
		cout << "WANT TO PLAY AGAIN? (Y/N)\n";
		string answer;
		cin >> answer;
		if (answer == "N" || answer == "n")
		{
			condition = false;
		}
	}
}