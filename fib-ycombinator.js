console.log(

((f, n) => f(f, n, 0, 1))(
  (self, count, current, next) => 
    count == 0 ? current : self(self, count-1, next, current+next)
  , 10)

)