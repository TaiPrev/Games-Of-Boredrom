#include <GL/glut.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <malloc.h>
#include <stdbool.h>


#include <iostream>

using namespace std;

double tablero[16];
double old_tablero[16];
double score;
bool ingame;

struct node
{
	double data;
	struct node *next;
};

class linked_list
{
	private:
		node *head, *tail;
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

	score += k.update();
	return k.get_array_double();
}

void update_memory(double original[16])
{
	for (int i=0; i<16; i++)
	{
		old_tablero[i] = original[i];
	}
}

void go_back()
{
	for (int i=0; i<16; i++)
	{
		tablero[i] = old_tablero[i];
	}
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
	srand(time(NULL));
	int r1 = (rand() % 16);

	while (tablero[r1]!=0){
		r1 = (rand() % 16);
	}
	tablero[r1] = (rand()%2+1)*2;
}

bool movement(int type)
{
	bool same_state = true;
	double aux_tablero[16];
	for (int k=0; k<16; k++){ aux_tablero[k] = tablero[k]; }
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
	if (!same_state)
	{
		update_memory(aux_tablero);
	}
	return same_state;
}

void reset_tablero()
{
	update_memory(tablero);
	ingame = true;
	srand(time(NULL));
	int r1 = (rand() % 16);
	int r2 = (rand() % 16);
	while (r2==r1){
		r2 = (rand() % 16);
	}

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
}

void print ()
{
	cout << "SCORE = " << score <<"\n";
	cout << tablero[0] << " ; " << tablero[1] << " ; " << tablero[2] << " ; " << tablero [3] << " ;\n";
	cout << tablero[4] << " ; " << tablero[5] << " ; " << tablero[6] << " ; " << tablero [7] << " ;\n";
	cout << tablero[8] << " ; " << tablero[9] << " ; " << tablero[10] << " ; " << tablero [11] << " ;\n"; 
	cout << tablero[12] << " ; " << tablero[13] << " ; " << tablero[14] << " ; " << tablero [15] << " ;\n"; 
}

void keyboard(unsigned char c, int x, int y)
{
	if (c == 27){
		exit(0);
	} 
	else {
		bool result = true;
		if ((c == 87) || (c == 119)){ //W & w
			result = movement(0);
		}
		else if ((c == 65) || (c == 97)){ //A & a
			result = movement(1);
		}
		else if ((c == 83) || (c == 115)){ //S & s
			result = movement(2);
		}
		else if ((c == 68) || (c == 100)){ //D & d
			result = movement(3);
		}
		else if ((c == 90) || (c == 122)){ //Z & z
			go_back();//undo the previous movement
			result = false;
		}
		if (!result)
		{
			if (!is_tablero_full())
			{
				add_new_value();
			}
		}
		else
		{
			if(is_tablero_full())
			{	//probably add some wait
				cout << "GAME OVER - POINTS:" << score << "\n";
				reset_tablero();
			}
		}
		glutPostRedisplay();
	}
	//print();
}

void render(void)
{	
	//2 OPTIONS, GAME BOARD AND RESET MENU?
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	//glColor3f(0.5f, 0.0f, 0.0f);

	float x[16] = {0.0f, 0.5f, 1.0f, 1.5f,
				   0.0f, 0.5f, 1.0f, 1.5f,
				   0.0f, 0.5f, 1.0f, 1.5f,
				   0.0f, 0.5f, 1.0f, 1.5f
				  };
	float y[16] = {0.0f, 0.0f, 0.0f, 0.0f,
				  -0.5f, -0.5f, -0.5f, -0.5f,
				  -1.0f, -1.0f, -1.0f, -1.0f,
				  -1.5f, -1.5f, -1.5f, -1.5f
				  };
	//DRAW THE CUBES
	//The game screen is compressed between axis X [-1,1] Y [-1,1]
	//Each cube thus occupies a range of |0.5| in heigh and width
	for (int i=0; i<16; i++){
		if (tablero[i]!=0){
			float colour_mod = log2(tablero[i]);
			if (colour_mod < 5) 
			{
				glColor3f(0.0f, 1.0f/colour_mod, 1.0f/colour_mod);
			}
			else if (colour_mod < 10)
			{
				glColor3f(1.0f/(fmod(colour_mod, 5) + 1), 0.0f, 1.0f/(fmod(colour_mod, 5)  + 1));
			}
			else{
				//glColor3f(1.0f/(fmod(colour_mod, 5) + 1), 1.0f/(fmod(colour_mod, 5)  + 1), 0.0f);
				glColor3f(1.0f/(fmod(colour_mod, 5) + 1), 0.0f, 0.0f);
			}
			
			/*
			glBegin(GL_QUADS); //Draws 1 cube, EXAMPLE
				glVertex3f(0.0, 0.0,0.0);
  				glVertex3f(1.0, 0.0,0.0);
  				glVertex3f(1.0,1.0,0.0);
  				glVertex3f(0.0,1.0,0.0);
			glEnd();
			*/
			glBegin(GL_QUADS);
				glVertex3f(-1.0+x[i], 1.0+y[i], 0.0);
  				glVertex3f(-0.5+x[i], 1.0+y[i], 0.0);
  				glVertex3f(-0.5+x[i], 0.5+y[i], 0.0);
  				glVertex3f(-1.0+x[i], 0.5+y[i], 0.0);
			glEnd();
		}
	}
	glutSwapBuffers();
}

int main (int argc, char **argv)
{
	//INITIAL DATA
	init();

	//MAKE WINDOW
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
    glutInitWindowSize(850, 850);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("2048");
    /* ... */
    glutDisplayFunc(render);
    glutKeyboardFunc(keyboard);
    //glutMouseFunc(mouse);

    glutMainLoop();
}