#include "pch.h"
#include <iostream>
#include <vector>
#include <algorithm>
#include <Windows.h>
#include <chrono>

using namespace std;

const float PI = 3.141592f;

int nScreenWidth = 120;
int nScreenHeight = 40;

float fPlayerX = 8.0f;
float fPlayerY = 8.0f;
float fPlayerA = 0.0f;

float fRotSpeed = 1.0f;
float fFOV = PI / 4.0f;
float fDepth = 16.0f;
float fStepSize = 0.1f; //Increment size for ray casting, decrease to increase resolution

int nMapHeight = 16;
int nMapWidth = 16;

float basic_distance_to_wall(float rayAngle, wstring map, bool* ptrbBoundary) 
{
	float fEyeX = sinf(rayAngle); //Unit vector for ray in player space
	float fEyeY = cosf(rayAngle);

	float dist = 0.0f;
	bool bHitWall = false;
	//bool bBoundary = false; //edges of the cells

	while (!bHitWall && dist < fDepth)
	{
		dist += fStepSize;

		int nTestX = (int)(fPlayerX + fEyeX * dist);
		int nTestY = (int)(fPlayerY + fEyeY * dist);

		//Test if ray is out of bounds
		if (nTestX < 0 || nTestX >= nMapWidth || nTestY < 0 || nTestY >= nMapHeight)
		{
			return fDepth; //Set distance to maximum depth
		}
		else
		{
			//Ray is inbounds so test to see if the ray cell is a wall block
			if (map[nTestY * nMapWidth + nTestX] == '#')
			{
				vector<pair<float,float>> p; //distance to perfect corner, dot
				for (int tx = 0; tx<2; tx++)
					for (int ty = 0; ty < 2; ty++)
					{
						float vy = (float)nTestY + ty - fPlayerY;
						float vx = (float)nTestX + tx - fPlayerX;
						float d = sqrt(vx*vx + vy*vy);
						float dot = (fEyeX*vx / d) + (fEyeY*vy / d); //normalized dot product
						p.push_back(make_pair(d, dot));
					}
				//Sort Pairs from closest to farthest, via a lamda function
				sort(p.begin(), p.end(), [](const pair<float, float> &left, const pair<float, float> &right) {return left.first < right.first; });

				float fBound = 0.01f; //in rads
				//Check if Ray has hit any of the boundaries of the cell
				if (acos(p.at(0).second) < fBound) *ptrbBoundary = true;
				if (acos(p.at(1).second) < fBound) *ptrbBoundary = true;
				//if (acos(p.at(2).second) < fBound) *ptrbBoundary = true; //3d space
				return dist;
			}
		}
	}
}

int main()
{
    // Create Screen Buffer
	wchar_t *screen = new wchar_t[nScreenWidth*nScreenHeight];
	HANDLE hConsole = CreateConsoleScreenBuffer(GENERIC_READ | GENERIC_WRITE, 0, NULL, CONSOLE_TEXTMODE_BUFFER, NULL);
	SetConsoleActiveScreenBuffer(hConsole);
	DWORD dwBytesWritten = 0;

	wstring map;

	//Oh look, it's my face, sideways, that is

	map += L"################";
	map += L"#..............#";
	map += L"#..............#";
	map += L"#......###.....#";
	map += L"#......###.....#";
	map += L"#......###.....#";
	map += L"#..............#";
	map += L"#..............#";
	map += L"#..............#";
	map += L"#..............#";
	map += L"#..............#";
	map += L"#..............#";
	map += L"#.......########";
	map += L"#..............#";
	map += L"#..............#";
	map += L"################";

	auto tp1 = chrono::system_clock::now();
	auto tp2 = chrono::system_clock::now();

	bool game_loop = true;

	//GAME LOOP
	while (game_loop)
	{
		tp2 = chrono::system_clock::now();
		chrono::duration<float> elapsedTime = tp2 - tp1;
		tp1 = tp2;
		float fElapsedTime = elapsedTime.count();

		//////////////////////////////////////////////////////////////////////////////
		//Controls
		//Escape
		if (GetAsyncKeyState(VK_ESCAPE))
			game_loop = false;
		//Handle CCW Rotation
		if (GetAsyncKeyState((unsigned short)'A') & 0x8000)
			fPlayerA -= fRotSpeed * fElapsedTime;
		if (GetAsyncKeyState((unsigned short)'D') & 0x8000)
			fPlayerA += fRotSpeed * fElapsedTime;
		if (GetAsyncKeyState((unsigned short)'W') & 0x8000)
		{
			fPlayerX += sinf(fPlayerA) * 5.0f * fElapsedTime;
			fPlayerY += cosf(fPlayerA) * 5.0f * fElapsedTime;
			if (map[(int)fPlayerY*nMapWidth + (int)fPlayerX] == '#')
			{
				fPlayerX -= sinf(fPlayerA) * 5.0f * fElapsedTime;
				fPlayerY -= cosf(fPlayerA) * 5.0f * fElapsedTime;
			}
		}
		if (GetAsyncKeyState((unsigned short)'S') & 0x8000)
		{
			fPlayerX -= sinf(fPlayerA) * 5.0f * fElapsedTime;
			fPlayerY -= cosf(fPlayerA) * 5.0f * fElapsedTime;

			if (map[(int)fPlayerY*nMapWidth + (int)fPlayerX] == '#')
			{
				fPlayerX += sinf(fPlayerA) * 5.0f * fElapsedTime;
				fPlayerY += cosf(fPlayerA) * 5.0f * fElapsedTime;
			}
		}
		//Strafing, aka, moving character just left or right
		if (GetAsyncKeyState((unsigned short)'Q') & 0x8000)  //left
		{	//flip 90 degrees (1.5708 in radians)
			fPlayerX -= sinf(fPlayerA + 1.5708f) * 5.0f * fElapsedTime;
			fPlayerY -= cosf(fPlayerA + 1.5708f) * 5.0f * fElapsedTime;
			if (map[(int)fPlayerY*nMapWidth + (int)fPlayerX] == '#')
			{
				fPlayerX += sinf(fPlayerA + 1.5708f) * 5.0f * fElapsedTime;
				fPlayerY += cosf(fPlayerA + 1.5708f) * 5.0f * fElapsedTime;
			}
		}
		if (GetAsyncKeyState((unsigned short)'E') & 0x8000) //right
		{
			fPlayerX += sinf(fPlayerA + 1.5708f) * 5.0f * fElapsedTime;
			fPlayerY += cosf(fPlayerA + 1.5708f) * 5.0f * fElapsedTime;

			if (map[(int)fPlayerY*nMapWidth + (int)fPlayerX] == '#')
			{
				fPlayerX -= sinf(fPlayerA + 1.5708f) * 5.0f * fElapsedTime;
				fPlayerY -= cosf(fPlayerA + 1.5708f) * 5.0f * fElapsedTime;
			}
		}
			
		//////////////////////////////////////////////////////////////////////////////
		
		for (int x = 0; x < nScreenWidth; x++)
		{
			//For each column, calculate, the projected ray angle into world space
			float fRayAngle = (fPlayerA - fFOV / 2.0f) + ((float)x / (float)nScreenWidth) * fFOV;
			bool bBoundary = false;
			float fDistanceToWall = basic_distance_to_wall(fRayAngle, map, &bBoundary); //0.0f;
			/*
			float fEyeX = sinf(fRayAngle); //Unit vector for ray in player space
			float fEyeY = cosf(fRayAngle);

			bool bHitWall = false;

			while (!bHitWall && fDistanceToWall < fDepth)
			{
				fDistanceToWall += fStepSize;

				int nTestX = (int)(fPlayerX + fEyeX * fDistanceToWall);
				int nTestY = (int)(fPlayerY + fEyeY * fDistanceToWall);

				//Test if ray is out of bounds
				if (nTestX < 0 || nTestX >= nMapWidth || nTestY < 0 || nTestY >= nMapHeight)
				{
					bHitWall = true; //Set distance to maximum depth
					fDistanceToWall = fDepth;
				}
				else
				{
					//Ray is inbounds so test to see if the ray cell is a wall block
					if (map[nTestY * nMapWidth + nTestX] == '#')
					{
						bHitWall = true;
					}
				}
			}
			*/
			//Calculate distance to ceiling and floor
			int nCeiling = (float)(nScreenHeight / 2.0) - nScreenHeight / ((float)fDistanceToWall);
			int nFloor = nScreenHeight - nCeiling;

			short nShade; // = ' ';

			for (int y = 0; y < nScreenHeight; y++)
			{
				if (y <= nCeiling) //Ceiling
					nShade = ' ';
				else if (y > nCeiling && y <= nFloor) //Wall
					if (bBoundary) nShade = ' ';
					else
					{
						if (fDistanceToWall <= fDepth / 4.0f)			nShade = 0x2588;	// Very close	
						else if (fDistanceToWall < fDepth / 3.0f)		nShade = 0x2593;
						else if (fDistanceToWall < fDepth / 2.0f)		nShade = 0x2592;
						else if (fDistanceToWall < fDepth)				nShade = 0x2591;
						else											nShade = ' ';		// Too far away
					}
																
				else //Floor
				{
					//Shade floor based on distance
					float b = 1.0f - (((float)y - nScreenHeight / 2.0f) / ((float)nScreenHeight / 2.0f));
					if (b < 0.25)		nShade = '#';
					else if (b < 0.5)	nShade = 'x';
					else if (b < 0.75)	nShade = '.';
					else if (b < 0.9)	nShade = '-';
					else				nShade = ' ';
				}
				screen[y*nScreenWidth + x] = nShade;
			}
			
		}


		//Display Stats
		swprintf_s(screen, 40, L"X=%3.2f, Y=%3.2f, A=%3.2f  FPS=%3.2f ", fPlayerX, fPlayerY, fPlayerA, 1.0f / fElapsedTime);

		//Display Map
		for (int nx = 0; nx < nMapWidth; nx++)
		{
			for (int ny = 0; ny < nMapHeight; ny++)
			{
				screen[(ny + 1)*nScreenWidth + nx] = map[ny*nMapWidth + nx];
			}
		}
		screen[((int)fPlayerY + 1) * nScreenWidth + (int)fPlayerX] = 'P';

		screen[nScreenWidth * nScreenHeight - 1] = '\0';
		WriteConsoleOutputCharacter(hConsole, screen, nScreenWidth * nScreenHeight, { 0, 0 }, &dwBytesWritten);
	}

	return 0;
}
