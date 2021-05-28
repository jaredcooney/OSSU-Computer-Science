(* Section 1 Practice Problems *)
(* Programming Languages, Part A (University of Washington) *)
(* Professor: Dan Grossman *)

(* Student: Jared Cooney *)
(* jaredcooney2@gmail.com *)

(* Language: Standard ML *)

(* ============================================================================= *)

(* 1. *)
(* adds the numbers in the list using alternating sign *)
fun alternate (numbers : int list) =
    #1 (foldl (fn (num, (acc, idx)) => if (idx mod 2) = 0
                                       then (acc + num, 1)
                                       else (acc - num, 0))
              (0, 0)
              numbers)


(* 2. *)
(* return a pair (min, max) containing the minimum and maximum numbers in the list *)
(* Assumes: the list is not empty *)
fun min_max (numbers : int list) =
    foldr (fn (num, (min, max)) => (if num < min then num else min,
                                    if num > max then num else max))
          (hd numbers, hd numbers)
          numbers


(* 3. *)
(* return a list of the partial sums of the numbers in the given list *)
(* Assumes: the list is not empty *)
fun cumsum (numbers : int list) =
    rev (foldl (fn (num, acc) => (num + (hd acc)) :: acc) [hd numbers] (tl numbers))


(* 4. *)
(* return the string "Hello there, ...!", where the ellipsis is 
   replaced by name, or by "you" if no name is given *)
fun greeting (name : string option) =
    "Hello there, "
    ^ (case name of NONE => "you" | SOME n => n)
    ^ "!"


(* 5. *)
(* repeat the ints in numbers according to the values with corresponding indices in repetitions *)
fun repeat (numbers : int list, repetitions : int list) =
    case (numbers, repetitions) of
        (_, []) => []
      | (num::nums', remaining::reps') => if remaining = 0
                                          then repeat(nums', reps')
                                          else num :: repeat(numbers, remaining - 1 :: reps')


(* 6. *)
(* if either argument is NONE, return NONE, else an option containing the sum of the two ints *)
fun addOpt (num1 : int option, num2 : int option) =
    case (num1, num2) of
        (SOME n1, SOME n2) => SOME (n1 + n2)
      | _ => NONE


(* 7. *)
(* sum all the ints that are present, else return NONE if there are none *)
fun addAllOpt (int_opts : (int option) list) =
    let val any_int = ref false

        fun sum_ints (int_opts : (int option) list) =
            case int_opts of
                [] => 0
              | SOME(i)::int_opts' => (any_int := true; i + sum_ints(int_opts'))
              | NONE::int_opts' => sum_ints(int_opts')

        val sum = sum_ints(int_opts)

    in if !any_int then SOME sum else NONE end


(* 8. *)
(* return true iff any element of the given list is true *)
val any = List.exists (fn b => b)


(* 9. *)
(* return false iff any element of the given list is false *)
val all = List.exists not


(* 10. *)
(* zips the elements of the two lists, stopping when either list is empty *)
fun zip (lst1 : int list, lst2 : int list) =
    case (lst1, lst2) of
        (hd1::lst1', hd2::lst2') => (hd1, hd2) :: zip(lst1', lst2')
      | _ => []  (* if either list is empty *)


(* 11. *)
(* zips the elements of the two lists, stopping when both lists are empty; *)
(* when one lists runs out, cycle back to the beginning of that list until the other is empty *)
fun zipRecycle (lst1 : int list, lst2 : int list) =
    case (lst1, lst2) of
        (_::_, _::_) =>
        let fun zipRecycle (xs : int list, ys : int list, lst1_empty : bool, lst2_empty : bool) =
                case (xs, ys, lst1_empty, lst2_empty) of
                    (_, _, true, true) => []
                  | ([], [], _, _) => []
                  | ([], _, _, _) => zipRecycle(lst1, ys, true, lst2_empty)
                  | (_, [], _, _) => zipRecycle(xs, lst2, lst1_empty, true)
                  | (x::xs', y::ys', _, _) => (x, y) :: zipRecycle(xs', ys', lst1_empty, lst2_empty)
        in zipRecycle(lst1, lst2, false, false) end
            
      | _ => []  (* if either initial list is empty *)


(* 12. *)
(* if the two lists are the same length, zip them and return result as an option; else NONE *)
fun zipOpt (lst1 : int list, lst2 : int list) =
    if length(lst1) = length(lst2) then SOME (zip(lst1, lst2)) else NONE


(* 13. *)
(* if target_str exists in the list of pairs, then return its paired int as an option *)
fun lookup (pairs : (string * int) list, target_str : string) =
    case (List.find (fn (str, num) => str = target_str) pairs) of
        NONE => NONE
      | SOME (s, i) => SOME i


(* 14. *)
(* separate the nonnegative numbers into one list and the negative numbers into
   another, preserving the relative order of the numbers in each list *)
val splitup = List.partition (fn num => num >= 0)


(* 15. *)
(* separate the numbers in the list into two lists, one containing the numbers >= threshold
   and the other containing those < threshold; preserves the relative order *)
fun splitAt (numbers : int list, threshold : int) =
    List.partition (fn num => num >= threshold) numbers


(* 16. *)
(* return true iff the list is sorted in nondecreasing order *)
fun isSorted (numbers : int list) =
    case numbers of
        first::(second::rest) => if first <= second
                                 then isSorted(second::rest)
                                 else false
      | _ => true


(* 17. *)
(* return true iff the list is sorted in either nondecreasing or nonincreasing order *)
fun isAnySorted (numbers : int list) =
    isSorted(numbers) orelse isSorted(rev(numbers))


(* 18. *)
(* merges the two lists into one nondecreasing-sorted list *)
(* Assumes: the two input lists are both sorted in nondecreasing order *)
fun sortedMerge (xs : int list, ys : int list) =
    case (xs, ys) of
        ([], _) => ys
      | (_, []) => xs
      | (x::xs', y::ys') => if x <= y
                            then x :: sortedMerge(xs', ys)
                            else y :: sortedMerge(xs, ys')


(* 19. *)
(* sorts the list of numbers in nondecreasing order using the QuickSort algorithm *)
fun qsort (numbers : int list) =
    case numbers of
        first::(second::rest) =>
        let val (at_or_above, below) = splitAt(second::rest, first)
        in sortedMerge([first], qsort(below) @ qsort(at_or_above)) end
            
      | _ => numbers  (* if numbers has fewer than two elements *)


(* 20. *)
(* return two lists by alternating adding elements of the given list to the output lists *)
fun divide (numbers : int list) =
    let fun aux (numbers : int list, (lst1, lst2) : int list * int list, alternator : bool) =
            case numbers of
                [] => (rev lst1, rev lst2)
              | num::numbers' => aux(numbers',
                                     if alternator then (num::lst1, lst2) else (lst1, num::lst2),
                                     not alternator)

    in aux(numbers, ([],[]), true) end


(* 21. *)
(* sorts the list of numbers in nondecreasing order using a less efficient algorithm *)
fun not_so_quick_sort (numbers : int list) =
    case numbers of
        first::second::rest =>
        let val (left, right) = divide(numbers)      
        in sortedMerge(not_so_quick_sort(left), not_so_quick_sort(right)) end
            
      | _ => numbers  (* if numbers has fewer than two elements *)


(* 22. *)
(* return a pair where the first element is the number of times k divides evenly *)
(* into n, and the second element is the result of dividing n by k that many times *)
fun full_divide (k : int, n : int) =
    let fun aux (n : int, count : int) =
            if (n mod k) <> 0
            then (count, n)
            else aux(n div k, count + 1)
                    
    in aux(n, 0) end


(* 23. *)
(* return a list of pairs (d, k) where each d is a prime factor of num0 and
   the corresponding k is the number of times it occurs as a factor *)
(* Assumes: the input number is a positive integer *)
fun factorize (num0 : int) =
    let fun aux (divisor : int, num : int, pairs : (int * int) list) =
            if divisor > (num0 div 2) + 1
            then pairs
            else  (* calculate how many times num can be evenly divided by divisor *)
                let val (occurrences, divided_num) = full_divide(divisor, num)
                in if occurrences > 0
                   then aux(divisor + 1, divided_num, (divisor, occurrences)::pairs)
                   else aux(divisor + 1, num, pairs)
                end

    in case aux(2, num0, []) of
           [] => if num0 <> 1 then [(num0,1)] else []
         | pairs => rev(pairs)
    end


(* 24. *)
(* given the factorization of a number (as returned by the above *)
(* function factorize), return the original number *)
fun multiply (factorization : (int * int) list) =
    case factorization of
        [] => 1
      | (factor, remaining_occurrences) :: rest =>
        if remaining_occurrences > 0
        then factor * multiply((factor, remaining_occurrences - 1) :: rest)
        else multiply(rest)


(* ============================================================================= *)
(* Challenge Problem *)

                     
(* remove duplicate values from the list; only the first instance of any given value remains *)
fun remove_duplicates (lst) =
    let fun aux (xs, visited, acc) =
            case xs of
                [] => acc
              | x::xs' => if List.exists (fn y => y = x) visited
                          then aux(xs', visited, acc)
                          else aux(xs', x::visited, x::acc)
                                  
    in rev(aux(lst, [], [])) end


(* return a list of possible combinations (lists) of the given numbers *)
fun gen_all_combos (numbers0 : int list) =
    let
        (* return the number of times num occurs in the numbers *)
        fun occurrences (num : int, numbers) =
            foldl (fn (n, acc) => if n = num then 1 + acc else acc) 0 numbers

        (* determines whether all occurrences of num have already been "used" in the combination *)
        fun all_used (num : int, combo : int list) =
            occurrences(num, combo) >= occurrences(num, numbers0)

        (* a map function that sorts each sublist in the given list *)
        val sort_combos = List.map qsort

        fun aux (numbers : int list,
                 acc : (int list) list,
                 currents : (int list) list,
                 nexts : (int list) list,
                 iters_remaining : int) =

            case (numbers, currents, iters_remaining) of
                (_, _, 0) => acc
              | (_, [], _) => let val pruned_nexts = (remove_duplicates o sort_combos) (rev(nexts))
                              in aux(numbers0, acc @ pruned_nexts, pruned_nexts, [], iters_remaining - 1)
                              end
              | ([], _::currents', _) => aux(numbers0, acc, currents', nexts, iters_remaining)
              | (num::numbers', combo::_, _) => aux(numbers',
                                                    acc,
                                                    currents,
                                                    (if all_used(num, combo)
                                                     then nexts
                                                     else (num::combo) :: nexts),
                                                    iters_remaining)


    in aux(numbers0, [], [[]], [], length(numbers0))
    end


(* 25. *)
(* given the factorization of a number (as returned by the function factorize), *)
(* return a list of all possible products returned from multiplying some *)
(* or all of the prime factors no more than the number of times they are available  *)
fun all_products (factorization : (int * int) list) =
    
    (* returns a flat list containing each factor as many times as it appears *)
    let fun list_factors (factorization : (int * int) list) =
            let fun aux (factorization : (int * int) list) =
                    case factorization of
                        [] => []
                      | (factor, remaining_occurrences)::factorization' =>
                        (if remaining_occurrences > 0
                         then factor :: aux((factor, remaining_occurrences - 1) :: factorization')
                         else aux(factorization'))

            in 1 :: aux(factorization) end

        (* maps each sublist of the given list to the product of its elements *)
        val multiply_combos = map (fn combo => (foldl (fn (num, acc) => num * acc) 1) combo)
                                  
    in (qsort o remove_duplicates o multiply_combos o gen_all_combos o list_factors) factorization
    end


