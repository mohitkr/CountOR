%-----------------------------------------------------------------------------
% Nurse scheduling problem
%
% Nina Narodytska
% 01.12.2007
%
% The nurse scheduling problem consists of assigning nurses to shifts to
% satisfy  nurses demand for each day.
% The model includes the following constraints:
% - each shift has a minimum required number of nurses
% - various regulation rules on each nurse schedule
% To run the model you need a data file from ./period_14 or ./period_28 to
% specify the minimum number of nurses required on each day[*]
%
%[*]Original benchmarks come from  http://www.projectmanagment.ugent.be/nsp.php
% They specify minimal required staff allocation for each shift and individual
% preferences for each nurse.  We ignore these preference and replace them with
% a set of constraints that model common workload restrictions for all nurses.
% The number of nurses in each instance is set to the maximal number of nurses
% required for any day over the period multiplied by 1.5.

% To test the model:
%
% nsp_1.mzn --data test.dzn
%-----------------------------------------------------------------------------

include "globals.mzn";
include "test.rules";

%-------------------------------------------------
% Model parameters
%-------------------------------------------------


int: n_nurses;         % The number of nurses
int: n_days;     % The scheduling period
int: n_shifts;         % The number of shifts:
                       %    1 stands for a day shift
                       %    2 stands for an evening shift
                       %    3 stands for a night shift
                       %    4 stands for day-off
int: n_bounds;          % The number of regulation rules

set of int: days           = 1..n_days;
set of int: shifts           = 1..n_shifts;
set of int: nurses           = 1..n_nurses;
set of int: bounds            = 1..n_bounds;

% additional regulation rules
array [bounds] of set of int: bounds_sets;


%-------------------------------------------------
% Model variables
%-------------------------------------------------

array [nurses, days, shifts] of var 0..1:  nurses_schedule;

array [nurses] of var int:  var1;
array [nurses] of var int:  var2;
array [nurses] of var int:  var3;
array [days] of var int:  var4;
array [days] of var int:  var5;
array [days] of var int:  var6;
array [shifts] of var int:  var7;
array [shifts] of var int:  var8;
array [shifts] of var int:  var9;
array [nurses, days] of var int:  var10;
array [nurses, shifts] of var int:  var11;
array [days, shifts] of var int:  var12;

constraint
    forall (i in nurses)(
        var1[i]=sum(non_zero(nurses_schedule,3,shifts),2)
    )

%-------------------------------------------------
% Model constraints
%-------------------------------------------------
%-----------------
%-- nurses demand
%------------------
%daily nurses demand
constraint(
       var10=array2d(nurses, days, [ max([x[i,j,k] | k in shifts]) | i in nurses, j in days]) 
       /\
       forall (i in nurses)(
           sum(j in days)(var10[i,j] >= bounds[2])
       )
    );

set of int: indices = 1 .. 3;
array[indices,indices,indices] of int: x =
    array3d(indices, indices, indices, [
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,

        11, 12, 13,
        14, 15, 16,
        17, 18, 19,

        21, 22, 23,
        24, 25, 26,
        27, 28, 29,
    ]);
array[indices,indices] of var int: y;

function array[int,int] of var int: nonzero3dto2d(array[int,int,int] of int: x, int: dim) =
    if dim == 1 then
        array2d(days, shifts, [ max([x[i,j,k] | i in nurses]) | j in days, k in shifts])
    else if dim == 2 then
        array2d(nurses, shifts, [ max([x[i,j,k] | j in days]) | i in nurses, k in shifts])
    else
        array2d(nurses, days, [ max([x[i,j,k] | k in shifts]) | i in nurses, j in days])
    endif;
    
function array[int] of var int: nonzero3dto1d(array[int,int,int] of int: x, array[int] of int: dim) =
    if dim == [0, 1] then
        array(shifts, [ max([x[i,j,k] | i in nurses, j in days]) | k in shifts])
    else if dim == [0, 2] then
        array(days, [ max([x[i,j,k] | i in nurses, k in shifts]) | j in days])
    else
        array(nurses, [ max([x[i,j,k] | j in days, k in shifts]) | i in nurses])
    endif;

function array[int,int] of var int: sum3dto2d(array[int,int,int] of int: x, int: dim) =
    if dim == 1 then
        array2d(days, shifts, [ sum([x[i,j,k] | i in nurses]) | j in days, k in shifts])
    else if dim == 2 then
        array2d(nurses, shifts, [ sum([x[i,j,k] | j in days]) | i in nurses, k in shifts])
    else
        array2d(nurses, days, [ sum([x[i,j,k] | k in shifts]) | i in nurses, j in days])
    endif;
    
function array[int] of var int: sum3dto1d(array[int,int,int] of int: x, array[int] of int: dim) =
    if dim == [0, 1] then
        array(shifts, [ sum([x[i,j,k] | i in nurses, j in days]) | k in shifts])
    else if dim == [0, 2] then
        array(days, [ sum([x[i,j,k] | i in nurses, k in shifts]) | j in days])
    else
        array(nurses, [ sum([x[i,j,k] | j in days, k in shifts]) | i in nurses])
    endif;
    
function array[int] of var int: sum2dto1d(array[int,int] of int: x, array[int] of int: dim) =
    if dim == [0, 1] then
        array(shifts, [ sum([x[i,j,k] | i in nurses, j in days]) | k in shifts])
    else if dim == [0, 2] then
        array(days, [ sum([x[i,j,k] | i in nurses, k in shifts]) | j in days])
    else
        array(nurses, [ sum([x[i,j,k] | j in days, k in shifts]) | i in nurses])
    endif;

constraint y = nonzero3d(x, 3);

% encoding for shifts
% 1 stands for a day shift
% 2 stands for an evening shift
% 3 stands for a night shift
constraint
    forall (j in shifts) (
            shifts_values[j] = j
    );

predicate day_distribute (int: i) = (
	 let {
	 	array [shifts] of var int: row_coverage =
	 		[coverage[i,j]| j in shifts]
	 } in
	 	distribute (row_coverage, shifts_values, [nurses_schedule[j,i]| j in nurses])
	);

% the distribute constraint
constraint
	forall (i in period)  (
		(day_distribute (i))
	);




solve satisfy;

