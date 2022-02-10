(* Section 3 Practice Problems *)
(* Programming Languages, Part A (University of Washington) *)
(* Professor: Dan Grossman *)

(* Student: Jared Cooney *)
(* jaredcooney2@gmail.com *)

(* Language: Standard ML *)

(* ============================================================================= *)

(* 1. *)
(* (’b -> ’c option) -> (’a -> ’b option) -> ’a -> ’c option *)
(* compose two functions with "optional" values; if
   either function returns NONE, the result is NONE *)
fun compose_opt f g x =
    case g(x) of
        NONE => NONE
      | SOME y => f y


(* 2. *)
(* (’a -> ’a) -> (’a -> bool) -> ’a -> ’a *)
(* if p(x) is true, recursively call do_until with f(x) as the third argument, else return x *)
fun do_until f p x =
    if p x
    then do_until f p (f(x))
    else x


(* 3. *)
(* factorial function for nonnegative integer inputs, implemented using do_until *)
fun factorial1 n =
    #2 (do_until (fn (x, acc) => (x + 1, acc * x))
                 (fn (x, _) => x <= n)
                 (1, 1))


(* 4. *)
(* (’’a -> ’’a) -> ’’a -> ’’a  ; recall that '' indicates an equality type *)
(* repeatedly apply f to the given value x until f(x) = x, then return that x *)
fun fixed_point f = do_until f (fn x => f(x) <> x)


(* 5. *)
(* (’a -> ’b) -> ’a * ’a -> ’b * ’b *)
(* a map function that operates on a pair of values *)
fun map_pair f (x, y) = (f x, f y)


(* 6. *)
(* (’b -> ’c list) -> (’a -> ’b list) -> ’a -> ’c list *)
(* apply f to each element in g(x) and concatenate all the resulting lists *)
fun app_all f g x =
    foldl (fn (y, acc) => acc @ f(y)) [] (g(x))


(* 7. *)
(* reimplementation of the built-in function List.foldr *)
fun foldr2 f init lst =
    let fun aux(acc, xs) =
            case xs of
                [] => acc
              | x::xs' => aux(f(x, acc), xs')

    in aux(init, rev lst) end


(* 8. *)
(* reimplementation of the built-in function List.partition *)
fun partition pred xs =
    let fun aux (xs, passing, failing) =
	    case xs of
		[] => (rev passing, rev failing)
	      | x::xs' => if pred x
			  then aux(xs', x::passing, failing)
			  else aux(xs', passing, x::failing)

    in aux(xs, [],[]) end


(* 9. *)
(* (’a -> (’b * ’a) option) -> ’a -> ’b list *)
(* takes a "seed" and a function that takes a seed and produces SOME (value, new_seed),
   or NONE if it is done seeding; return a list of the values generated in the process *)
fun unfold f seed =
    case f(seed) of
        NONE => []
      | SOME (value, new_seed) => value :: (unfold f new_seed)


(* 10. *)
(* factorial function for nonnegative integer inputs,
   implemented using unfold and List.foldl *)
fun factorial2 n =
    foldl (op * )
          1
          (unfold (fn x => if x > 1 then SOME (x, x-1) else NONE) n);

(* 11. *)
(* reimplementation of the built-in function List.map, using List.foldr *)
fun map2 f =
    foldr (fn (x, acc) => f(x) :: acc) []


(* 12. *)
(* reimplementation of the built-in function List.filter, using List.foldr *)
fun filter2 f =
    foldr (fn (x, acc) => if f(x) then x::acc else acc) []


(* 13. *)
(* reimplementation of the built-in function List.foldl using List.foldr *)
fun foldl2 f init =
    (foldr (fn (x, acc) => f(x, acc)) init) o rev


(* ====================================================== *)
(* 14. *)

(* polymorphic binary tree structure; internal nodes hold values, leaves do not *)
datatype 'a tree = Leaf
                 | Node of {value : 'a, left : 'a tree, right : 'a tree}


(* map function for binary trees *)
fun tree_map f tre =
    case tre of
        Leaf => Leaf
      | Node {value=value, left=left, right=right} =>
        Node {value = f(value), left = tree_map f left, right = tree_map f right}


(* fold function for binary trees *)
fun tree_fold f init tre =
    case tre of
        Leaf => init
      | Node {value=value, left=left, right=right} =>
        f(value, tree_fold f init left, tree_fold f init right)


(* filter function for binary trees *)
fun tree_filter f tre =
    case tre of
        Leaf => Leaf
      | Node {value=value, left=left, right=right} =>
        if f(value)
        then Node {value=value, left = tree_filter f left, right = tree_filter f right}
        else Leaf
