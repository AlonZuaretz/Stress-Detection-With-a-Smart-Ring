function a = processAcc(acc)
    a.x = (acc(:,1)-128)/64;
    a.y = (acc(:,2)-128)/64;
    a.z = (acc(:,3)-128)/64;
    a.M = sqrt(a.x.^2+a.y.^2+a.z.^2);
end