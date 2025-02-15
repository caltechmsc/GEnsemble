      program exp6
c
c     driver for testing abc2rdz
c
c     wag 20nov93
c
      implicit none
      real*8 a,b,c,Re,De,zeta
      integer option
      real*8 ev2kcal
      parameter (ev2kcal=23.0603)
c
 11   write(6,1008) 
 1008 format(2x,'convert E=A*exp(-C*r) - B/R**6 to form for POLYGRAF')
      write(6,1009) 
 1009 format(2x'options:blank-default:input,output in kcal/mol,A'/
     $       2x,'        110: input in eV, output in kcal/mol'/
     $       2x,'        001: input 1/c'/
     $       2x,'        111: combine above two'/
     $       2x,'       1000: b=0, pure exponential'/
     $       2x,'       1001: combine b=0 and 1/c options'/
     $       2x,'       1111: combine all of above options'/
     $       2x,'        -1 : terminate (normally cycles to new case)')
c
      read(5,*) option
      if (option.lt.0) stop
c
      if (option/1000.eq.0) then
         write(6,*) ' input A,B,C where E=A*exp(-C*r) - B/R**6'
         read(5,*) a,b,c
         write(6,1003) a,b,c
 1003    format(2x,'input:a,b,c=',3f15.5)
      else
         write(6,1007) 
 1007    format(2x,'input A,C where E=A*exp(-C*r) and reference ',
     $        'distance Re for final form'/
     $        2x,'E=De*exp[z*(1-R/Re)]')
         read(5,*) a,c,Re
         write(6,1006) a,c,Re
 1006    format(2x,'input:a,c,Re=',3f15.5)
      endif
c
      if (mod(option,10).eq.1) then
         write(6,*) 'will use inverse of c'
         c=1.0/c
      endif
c
      if (mod(option/10,100).eq.11) then
         write(6,*) 
     $        'will convert a and b from eV to kcal/mol using 23.0603'
         a=a*ev2kcal
         b=b*ev2kcal
      endif
c
      if (option/1000.eq.0) then
         call abc2rdz(a,b,c,Re,De,zeta)
         write(6,1004) Re,De,zeta
 1004    format(
     $       2x,'E/De = [6/(z-6)]*exp[z*(1-rho)] - [z/(z-6)]/rho**6,',
     $          '  where rho=R/Re'/
     $       2x,'Re=',f10.5,' A'/
     $       2x,'De=',f10.5,' kcal/mol'/
     $       2x,'z =',f10.5/)
      else
c        pure exponential
         zeta=c*Re
         De=a*exp(-zeta)
         write(6,1005) Re,De,zeta
 1005    format(
     $       2x,'E/De=exp[z*(1-rho)],  where rho=R/Re'/
     $       2x,'Re=',f10.5,' A'/
     $       2x,'De=',f10.5,' kcal/mol'/
     $       2x,'z =',f10.5)
      endif
      write(6,*) '_________________________________________________'
      write(6,*) ' '
c
      go to 11
      end
*****************************************************************************
      subroutine abc2rdz(a,b,c,Re,De,zeta)
*****************************************************************************
c
c     convert E=A*exp(-C*r) - B/R**6
c     to      E/De=[6/(z-6)]*exp[z*(1-rho)] - [z/(z-6)]/rho**6
c
      implicit none
      real*8 a,b,c,Re,De,zeta
      real*8 factor,term,error,errderiv,dltzet,bcheck,logfact,thresh
      integer itermax,iter,ibout
      parameter (itermax=100)
      parameter (thresh=0.000001d0)
      parameter (ibout=6)
c
      factor=a/(6.0*b*c**6)
      logfact=log(factor)
      zeta=12.0
      iter=1
 11   term=7.0*log(zeta)
      error=zeta-term-logfact
      errderiv=1.0-7.0/zeta
      dltzet=-error/errderiv
      if (abs(dltzet).lt.thresh) then
         write(ibout,1001) iter
 1001    format(2x,'calculation converged in ',i4,' iterations')
         go to 101
      elseif (iter.gt.itermax) then
         write(ibout,1002) iter,error
 1002    format(2x,'calculation did not converge in ',i4,' iterations',
     $        'error in zeta is',f10.5)
         go to 101
      endif
      iter=iter+1
      zeta=zeta+dltzet
      go to 11
c
c     calculation finished
c
 101  Re=zeta/c
      De=a*(zeta/6.0-1.0)*exp(-zeta)
c
      bcheck=(zeta/(zeta-6))*De*Re**6
!      if (abs(bcheck-b).gt.0.0001) write(ibout,1003) bcheck,b
      write(ibout,1003) bcheck,b
 1003 format(2x,'output Re,De,zeta correspond to b=',f12.6,
     $     ' input was ',f12.6)
c
      return
      end
