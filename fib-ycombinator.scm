((lambda (f n)
   (f f n 0 1))
 (lambda (self count a b)
   (if (= count 0)
       a
       (self self (- count 1) b (+ a b))))
 10)
