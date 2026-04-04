console.log(

((f, n) => f(f, n, 0, 1))(
  (self, count, a, b) => 
    count == 0 ? a : self(self, count-1, b, a+b)
  , 10
)

)