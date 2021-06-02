(* Section 2 Practice Problems *)
(* Programming Languages, Part A (University of Washington) *)
(* Professor: Dan Grossman *)

(* Student: Jared Cooney *)
(* jaredcooney2@gmail.com *)

(* Language: Standard ML *)

(* ============================================================================= *)

type student_id = int
type grade = int  (* must be an integer in [0, 100] *)
type final_grade = { id : student_id, grade : grade option }
datatype pass_fail = pass | fail


(* 1. *)
(* final_grade -> pass_fail *)
(* return pass iff the grade is SOME i where i >= 75, else fail *)
fun pass_or_fail {grade=score, id=id} =
    case score of
        NONE => fail
      | SOME g => if g >= 75 then pass else fail


(* 2. *)
(* return true iff the grade is SOME i where i >= 75 *)
fun has_passed grade_record =
    case pass_or_fail(grade_record) of
        pass => true
      | fail => false


(* 3. *)
(* return the number of students who have a grade of SOME i where i >= 75 *)
fun number_passed final_grades =
    foldl (fn (fg, acc) => acc + (if has_passed(fg) then 1 else 0)) 0 final_grades


(* 4. *)
(* (pass_fail * final_grade) list -> int *)
(* return the number of final_grades paired with the wrong pass_fail value *)
fun number_misgraded pairs =
    foldl (fn ((pf, fg), acc) => acc + (if pass_or_fail(fg) <> pf then 1 else 0))
          0
          pairs


(* ============================================================================= *)

datatype 'a tree = leaf
                 | node of { value : 'a, left : 'a tree, right : 'a tree }

datatype flag = leave_me_alone | prune_me


(* 5. *)
(* return the height of the tree *)
fun tree_height tre =
    case tre of
        leaf => 0
      | node {value=_, left=lft, right=rgt} => 1 + Int.max(tree_height(lft), tree_height(rgt))


(* 6. *)
(* return the sum of all node values in the tree *)
fun sum_tree int_tree =
    case int_tree of
        leaf => 0
      | node {value=valu, left=lft, right=rgt} => valu + sum_tree(lft) + sum_tree(rgt)


(* 7. *)
(* replace all nodes that have value prune_me with leaves (including their descendants) *)
fun gardener flag_tree =
    case flag_tree of
        leaf => leaf
      | node{value=prune_me, left=_, right=_} => leaf
      | node{value=leave_me_alone, left=lft, right=rgt} =>
        node{value=leave_me_alone, left=gardener(lft), right=gardener(rgt)}


(* 8a. *)
(* reimplementation of the built-in take function *)
fun take2 (xs, idx) =
    case (xs, idx) of
        (_, 0) => []
      | (x::xs', _) => x :: take2(xs', idx - 1)


(* 8b. *)
(* reimplementation of the built-in drop function *)
fun drop2 (xs, idx) =
    case (xs, idx) of
        (_, 0) => xs
      | (x::xs', _) => drop2(xs', idx - 1)

(* 8c. *)
(* reimplementation of the built-in concat function *)
fun concat2 lists =
    foldl (fn (lst, acc) => acc @ lst) [] lists


(* 8d. *)
(* reimplementation of the built-in getOpt function *)
fun getOpt2 (opt, a) =
    case opt of
        SOME v => v
      | _ => a


(* 8e. *)
(* reimplementation of the built-in join function *)
fun join2 opt_opt =
    case opt_opt of
        SOME (SOME v) => SOME v
      | _ => NONE


(* ============================================================================= *)

datatype nat = ZERO | SUCC of nat
exception Negative


(* 9. *)
(* return true iff the nat is positive (i.e. greater than zero) *)
fun is_positive nat_num =
    case nat_num of ZERO => false
                  | SUCC _ => true


(* 10. *)
(* return the nat number that comes immediately before num *)
fun pred nat_num =
    case nat_num of
        SUCC n => n
      | ZERO => raise Negative


(* 11. *)
(* given a nat number, return the corresponding integer *)
fun nat_to_int nat_num =
    case nat_num of
        ZERO => 0
      | SUCC n => 1 + nat_to_int(n)


(* 12. *)
(* given a nonnegative integer, return the corresponding nat number *)
fun int_to_nat num =
    case num of
        0 => ZERO
      | _ => if num > 0
             then SUCC (int_to_nat(num-1))
             else raise Negative


(* 13. *)
(* without using nat_to_int or int_to_nat, add the two
    nat numbers and return the result as a nat *)
fun add (nat1, nat2) =
    case (nat1, nat2) of
        (ZERO, ZERO) => ZERO
      | (SUCC n1, ZERO) => SUCC (add(n1, ZERO))
      | (ZERO, SUCC n2) => SUCC (add(ZERO, n2))
      | (SUCC n1, SUCC n2) => (SUCC o SUCC o add) (n1, n2)


(* 14. *)
(* without using nat_to_int or int_to_nat, subtract
   nat2 from nat1 and return the result as a nat *)
fun sub (nat1, nat2) =
    case (nat1, nat2) of
        (_, ZERO) => nat1
      | (ZERO, SUCC _) => raise Negative
      | (SUCC n1, SUCC n2) => sub(n1, n2)


(* 15. *)
(* without using nat_to_int or int_to_nat, multiply
   nat1 by nat2 and return the result as a nat *)
fun mult (nat1, nat2) =
    case (nat1, nat2) of
        (ZERO, _) => ZERO
      | (_, ZERO) => ZERO
      | (SUCC _, SUCC n2) => add(nat1, mult(nat1, n2))


(* 16. *)
(* return true iff nat1 < nat2 *)
fun less_than (nat1, nat2) =
    case (nat1, nat2) of
        (ZERO, SUCC _) => true
      | (_, ZERO) => false
      | (SUCC n1, SUCC n2) => less_than(n1, n2)


(* ============================================================================= *)

datatype intSet =
         Elems of int list  (* list of integers, possibly with duplicates to be ignored *)
         | Range of {from : int, to : int}  (* integers in the range [from, to] *)
         | Union of intSet * intSet  (* union of the two sets *)
         | Intersection of intSet * intSet  (* intersection of the two sets *)


(* remove duplicate elements from the list; only the first instance of any given number remains *)
fun remove_duplicates numbers =
    let fun aux (numbers, visited, acc) =
            case numbers of
                [] => acc
              | num::numbers' => if List.exists (fn n => n = num) visited
                                 then aux(numbers', visited, acc)
                                 else aux(numbers', num::visited, num::acc)

    in (List.rev o aux) (numbers, [], [])
    end


(* return true iff there is at least one element that appears in both lists *)
fun any_common_element (xs, ys) =
    foldl (fn (x, acc) => (List.exists (fn y => y = x) ys) orelse acc) false xs


(* return a list containing only the elements that
   appear in both xs and ys, without duplicates *)
fun only_common (xs, ys) =
    let fun aux (xs, acc) =
            case xs of
                [] => acc
              | x::xs' => if (List.exists (fn y => y = x) ys)
                             andalso not (List.exists (fn a => a = x) acc)
                          then aux(xs', x::acc)
                          else aux(xs', acc)

    in aux(xs, []) end


(* 17. *)
(* return a list containing the elements of the given set, without duplicates *)
fun toList set =
    case set of
        Elems ints => remove_duplicates(ints)
      | Range {from=from, to=to} => (List.tabulate(to - from + 1, (fn n => n + from))
                                     handle Size => [])
      | Union (sub1, sub2) => remove_duplicates(toList(sub1) @ toList(sub2))
      | Intersection (sub1, sub2) => only_common(toList(sub1), toList(sub2))


(* 18. *)
(* return true iff the set is empty *)
fun isEmpty set =
    case set of
        Elems ints => ints = []
      | Range {from=from, to=to} => from > to
      | Union (sub1, sub2) => isEmpty(sub1) andalso isEmpty(sub2)
      | Intersection (sub1, sub2) => not (any_common_element(toList(sub1), toList(sub2)))


(* 19. *)
(* return true iff num is an element in the given intSet *)
fun contains (set, num) =
    List.exists (fn i => i = num) (toList(set))
