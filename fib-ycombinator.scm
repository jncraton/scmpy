((lambda (f n)
   (f f n 0 1))
 (lambda (self count current next)
   (if (= count 0)
       current
       (self self (- count 1) next (+ current next))))
 10)
